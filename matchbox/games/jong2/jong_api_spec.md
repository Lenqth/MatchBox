# 自分のターン

Server : { "type" : "your_turn" }
Reply : {}

# 鳴きチェック

Server : { "type" : "claim_command" , "timeout" : timeout }
Reply : {}

# のこり更新

Server : { "type" : "deck_left" , "deck_left" : deck_left }

# 手牌公開

Server : { "type":"open_hand" , "hand" : hand }
hand := [ pid -> pid の手札 ]

# あがり

Server : { "type":"agari" }
Reply : {} (OK 押したら)

# 流局

Server : { "type":"gameover" }
Reply : {} (OK 押したら)

# プレイヤーの鳴き追加

Server : {}

# プレイヤーの捨牌情報変更

Server : { "type" : "modify_trash" , "pid" : pid , "pos" : pos }

# 終わり

Server : { "type" : "final_result" }

# リセット

Server : { "type":"reset" }
