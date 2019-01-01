import {Observable,Observer,Subject, Subscription} from "rxjs";
import {shareReplay, distinctUntilChanged } from 'rxjs/operators';

export class SubjectWebSocket<T> extends Subject<T> {
  public ws : WebSocket;
  public connected : Observable<boolean> ;
  private conn_obs? : Observer<boolean> ;
  constructor(
    src:string) {

    super();
    this.ws = new WebSocket(src);
    this.conn_obs = undefined;
    this.ws.addEventListener(
      "open",
      () => { this.conn_obs!.next(true) },{ once: true } );
    this.ws.addEventListener(
      "close",
      () => { this.complete();this.conn_obs!.next(false) },{ once: true } );
    this.ws.addEventListener(
      "error",
      (e) => { this.error(e);this.conn_obs!.next(false) });
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
    this.ws.send(body);
  }

  async send(body:any){
    this.ws.send(JSON.stringify(body));
  }

  async waitReady(){
    var o : Subscription|undefined = undefined ;
    try{
      await new Promise( (resolve:Function,reject:Function) => 
        o = this.connected.subscribe(
          (x) => {if(x){ resolve() }} , () => {reject()} , () => {reject()}
        ) );
    }finally{
      (o != undefined) && o!.unsubscribe()
    }
  }
}