-- ----------------------------admin-func---------------------------------------------
select pid, now()-pg_stat_activity.query_start AS duration, query, state, datname, usename
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '1 minutes';
select pg_terminate_backend(69482);
select * from pg_stat_activity;

select * from live d limit 10;
SELECT TO_CHAR(NOW(), "dd-mm-yyyy");
select
    to_char(now(),'YYYY/MM/DD HH24:MM:SS'),
    to_char(now(),'YYYY-MM-DD');
-- ---------------------------------call-procedure-----------------------------------------
call prepare_bi();   
   
-- ----------------------------------pre-procedures----------------------------------------------
drop table if exists live_email_issues ;
create table if not exists live_email_issues as
select *
, case when "Subject" similar to '%(Failure|Undeliverable)%' then 1 else 0 end bounce
, case when "From" like '%complaint%' then 1 else 0 end complaints
from live l 
where "Subject" similar to '%(Failure|Undeliverable)%'  or "From" like '%complaint%';
	
drop table if exists live_metric_domain ;
create table if not exists live_metric_domain as
select
	to_char("timestamp_filename",'YYYY-MM-DD') month_sent
	,case when "direction" = 'outbound' then regexp_replace(regexp_replace("From", '^.*@', ''),'>','')
	else regexp_replace(regexp_replace("To", '^.*@', ''),'>','') end sender_domain_live
	,case when "categories" like '%warming%' then 1 else 0 end warming
	-- ,"direction"
	,sum(1) total_traffic
	,sum(case when direction='inbound' then 1 else 0 end) inbound
	,sum(case when direction='outbound' then 1 else 0 end) outbound
	,sum(case when "In-Reply-To" = '' then 0 else 1 end) in_reply
	-- ,sum(case when "Subject" like 'Re:%' then 1 else 0 end) reply_subj
	,sum(case when "References" = '' then 0 else 1 end) reference -- too high
	,sum(case when "Subject" like '%Failure%' then 1 
	when "Subject" like '%Undeliverable%' then 1 else 0 end) bounce
	,sum(case when "From" like '%complaint%' then 1 else 0 end) complaints
	-- ,sum(case when "feedback_text" = '' then 0 else 1 end) feedback
	,sum(case when "categories" like '%abuse%' then 1 else 0 end) abuse
	,sum(case when "categories" like '%reply%' then 1 else 0 end) reply
	,sum(case when "categories" like '%status_notification%' then 1 else 0 end) notification
from live d 
-- WHERE "To" NOT LIKE '%postmaster@%' 
group by 1,2,3
order by 1,2,3;

drop table if exists client_domain;
create temporary table if not exists client_domain as
with a as (select regexp_replace("Mailbox",'^.*@','') sender_domain, "ClientUsername" from client_mail mc)
select sender_domain, max("ClientUsername") "ClientUsername" from a 
group by 1 order by 1;

drop table if exists live_performance_address;
create table if not exists live_performance_address as
with a as (select
	sender_domain_live
	,month_sent
	,warming
	,sum(total_traffic) total
	,sum(bounce)/nullif(sum(outbound),0) bounce_rate
	,sum(reference)/nullif(sum(outbound),0) reference_rate
	,sum(reply)/nullif(sum(outbound),0) reply_rate
	,sum(abuse)/nullif(sum(outbound),0) abuse_rate
	,sum(complaints)/nullif(sum(outbound),0) complaints_rate
	,sum(notification)/nullif(sum(outbound),0) notification_rate
-- spam rate → incoming Bounces Emails as Spam Block CODES / outgoing Sent Emails
from live_metric_domain dm where outbound > 0
group by 1,2,3 order by 1,2,3)
, b as (select * from client_domain)
select a.*, b.* from a
left join b on a.sender_domain_live = b.sender_domain
 -- and sender_domain not like '%lightmeter%' 
;

drop table if exists live_performance_domain ;
create table if not exists live_performance_domain as
with c as (
	select * 
	from live_metric_domain a 
	left join client_domain b on a.sender_domain_live = b.sender_domain
	where outbound > 1) 
	select "ClientUsername"
	,month_sent
	,warming
	,sum(total_traffic) total
	,sum(bounce)/nullif(sum(outbound),0) bounce_rate
	,sum(reference)/nullif(sum(outbound),0) reference_rate
	,sum(reply)/nullif(sum(outbound),0) reply_rate
	,sum(abuse)/nullif(sum(outbound),0) abuse_rate
	,sum(complaints)/nullif(sum(outbound),0) complaints_rate
-- spam rate → incoming Bounces Emails as Spam Block CODES / outgoing Sent Emails
from c 
group by 1,2,3 order by 1,2,3;

-- select month_sent,avg(bounce_rate) bounce,avg(reference_rate) reference,avg(reply_rate) reply,avg(complaints_rate) complaints
-- from performance_domain dm group by 1 order by 1;

drop table dovecot_domain_metric ;
create table if not exists dovecot_domain_metric as
select
	to_char("Date",'YYYY-MM') month_sent
	-- substring("Date",1,7) month_sent -- postfix
	,case when "folder" = '.sent-mails' then regexp_replace(regexp_replace("From", '^.*@', ''),'>','')
	else regexp_replace(regexp_replace("To", '^.*@', ''),'>','') end sender_domain
	,sum(1) total_traffic
	,sum(case when "In-Reply-To" = '' then 0 else 1 end) in_reply
	-- ,sum(case when "Subject" like 'Re:%' then 1 else 0 end) reply_subj
	,sum(case when "References" = '' then 1 else 0 end) reference
	,sum(case when "Subject" like '%Failure%' then 1 else 0 end) bounce
--	,sum(case when "bounce_text" = '' then 0 else 1 end) bounce -- "message/delivery-status"
	,sum(case when "feedback_text" = '' then 1 else 0 end) feedback -- "message/feedback-report" Feedback-Type: abuse 
	,sum(case when "From" like '%complaint%' then 1 else 0 end) complaints
	,sum(case when "folder" = '.Sent' then 1 else 0 end) sent 
	,sum(case when "folder" = '.sent-mails' then 1 else 0 end) sent_mail 
	,sum(case when "folder" = '.To Follow' then 1 else 0 end) to_follow_warming
	,sum(case when "folder" = 'Inbox' then 1 else 0 end) inbox
-- filter category INCLUDE = EXCLUDE warming emails, only real tooling sending
-- Diagnostic-Code: Needs to create a rule
-- HEADER Feedback-Type: abuse = to validate?
-- Body use the abuse word?
from dovecot d 
group by 1,2
order by 1,2;

drop table dovecot_domain_performance ;
create table if not exists dovecot_domain_performance as
select
	month_sent
	,"sender_domain"
	,sum(sent_mail) sent
	,sum(bounce)/nullif(sum(sent_mail),0) bounce_rate
	-- ,sum(reply_subj)/nullif(sum(sent_mail),0) reply_rate
	,sum(in_reply)/nullif(sum(sent_mail),0) inReply_rate
	,sum(to_follow_warming)/nullif(sum(sent_mail),0) warming_rate
	,sum(complaints)/nullif(sum(sent_mail),0) complaints_rate
from dovecot_domain_metric dm  
where sent_mail > 10
group by 1,2
order by 1,2;

drop table if exists mailreach_performance_client;
create table if not exists mailreach_performance_client as
with a as (select
	"domain"
	,to_char("time",'YYYY-MM') month_sent
	,provider
	,sum(sent) sent, sum(received) received, sum(inbox) inbox, sum("others") "others", sum(categories) categories
-- spam rate → incoming Bounces Emails as Spam Block CODES / outgoing Sent Emails
from mailreach_volume dm 
group by 1,2,3 order by 1,2,3)
, b as (select * from client_domain)
select a.*, b.* from a
left join b on a."domain" = b.sender_domain
 -- and sender_domain not like '%lightmeter%' 
;


-- check definitions
-- select * from domain_metric dm where bounce > 0 and sender_domain_live like '%agency%';
-- --------------------------------------------anonym-views------------------------------------
-- ALTER TABLE live_zip RENAME TO live;
DROP MATERIALIZED VIEW view_name;
CREATE MATERIALIZED VIEW dovecot_anym AS
SELECT 'REDACTED'::TEXT AS firstname,anon.generalize_int4range(zipcode,1000) AS zipcode,anon.generalize_daterange(birth,'decade') AS birth,disease FROM dovecot;
-- REFRESH MATERIALIZED VIEW view_name;
-- CREATE TABLE IF NOT EXISTS products (id SERIAL,name TEXT NOT NULL,price NUMERIC(10,2) NOT NULL DEFAULT 0.00, CONSTRAINT products_pkey PRIMARY KEY (id));