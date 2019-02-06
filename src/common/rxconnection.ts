import {Observable,Observer,Subject, Subscription} from "rxjs";
import {shareReplay, distinctUntilChanged , retryWhen} from 'rxjs/operators';

export class SubjectWebSocket<T> extends Subject<T> {

  public ws? : WebSocket ;
  public connected? : Observable<boolean> ;
  private conn_obs? : Observer<boolean> ;
  public src: string;
  constructor(
    src:string) {
    super();
    this.src = src;
    this.ws = undefined;
    this.connected = undefined;
    this.conn_obs = undefined;
    this.reset();
  }

  private handle_error(e : Event) {
    this.error(e);
    this.conn_obs!.next(false);
  }

  async reset(){
    try{
      (this.ws != undefined) && this.ws!.close();
    }catch(e){}
    this.ws = new WebSocket(this.src);
    this.conn_obs = undefined;
    this.ws.addEventListener(
      "open",
      () => { this.conn_obs!.next(true) },{ once: true } );
    this.ws.addEventListener(
      "close",
      () => {
        this.complete();
        this.conn_obs!.next(false)
      },{ once: true } );
    this.ws.addEventListener(
      "error",
      (e) => {  
        this.handle_error(e);
      });
    this.ws.addEventListener(
      "message",
      (m) => { this.next(m.data) });

    this.connected = new Observable((observer: Observer<boolean>) => {
      this.conn_obs = observer;
    }).pipe(
      shareReplay(1),
      distinctUntilChanged()
    );
  }

  async sendRaw(body:string){
    this.ws!.send(body);
  }

  async send(body:any){
    this.ws!.send(JSON.stringify(body));
  }

  async waitReady(){
    var o : Subscription|undefined = undefined ;
    try{
      await new Promise( (resolve:Function,reject:Function) => 
        o = this.connected!.subscribe(
          (x) => {if(x){ resolve() }} , () => {reject()} , () => {reject()}
        ) );
    }finally{
      (o != undefined) && o!.unsubscribe()
    }
  }
}

export class PollingSocket<T> extends Subject<T> {
  interval: number;
  timer: NodeJS.Timeout;
  skipping: boolean = false;
  _internal_socket: SubjectWebSocket<T>;
  
  constructor(src:string,interval:number=5000) {
    super();
    this.interval = interval;
    this.timer = setInterval( this.tick , this.interval );
    this._internal_socket = new SubjectWebSocket<T>(src);
    var r = this._internal_socket.pipe( retryWhen( this.retry ) );
    this.subscribe(  )
  }  
  private retry( o : Observable<T> ) : Observable<T> {
    this._internal_socket.reset();
    return o;
  }

  async send(body:any){
    this._internal_socket.send(body);
  }

  private tick() : void {
    if(!this.skipping){
      this.send({"type":"polling"});
    }
  }

  dispose(){
    clearInterval(this.timer);
  }
}