# db
bounces.db:
* emails: id|email|decision|zerobounce|neverbounce
* goose_db_version: id_version | is_applied - library for migration: metadata
* queried: email_id | send_id
* senders: id | mail

l3m.db:
* compliants: received|sender|rcpt|feedback|original_email - rcpt recipient
* notifs: mbox_lm|mbox_ext
* replies: id|received|mailfrom|mailto|subject|status|email
* spammed: since|mailfrom|mailto|topmx|matched|comment - topmx: spammed by, service labelling the email as spam
* recipients: email|creation|relay|comment|matched|sender - matched: regex with a status label, error code; 
* senders: email|creation|relays - relay: email distributor
* transport_cache (hash): id|created_at|transport|recipient - trasport: configuration for an handover to a different distributor (postfix) like frequency; hash table 


logtracker.db: auxiliary table by the system 
* connection_data: id|connection_id|key|value
* pids: id|pid|usage_counter|host
* queues: id|connection_id|usage_counter|messageid_id|queue
* 

# jobs
