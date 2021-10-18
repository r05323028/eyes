Search.setIndex({docnames:["index","sources/api/celery","sources/api/config","sources/api/crawler","sources/api/data","sources/api/db","sources/api/exception","sources/api/job","sources/api/ml","sources/api/schema","sources/guides/installation","sources/guides/send_jobs","sources/guides/train_models"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["index.rst","sources/api/celery.rst","sources/api/config.rst","sources/api/crawler.rst","sources/api/data.rst","sources/api/db.rst","sources/api/exception.rst","sources/api/job.rst","sources/api/ml.rst","sources/api/schema.rst","sources/guides/installation.rst","sources/guides/send_jobs.rst","sources/guides/train_models.rst"],objects:{"eyes.celery.crawler":{tasks:[1,0,0,"-"]},"eyes.celery.crawler.tasks":{CrawlerTask:[1,1,1,""],crawl_dcard_board_list:[1,4,1,""],crawl_dcard_post:[1,4,1,""],crawl_ptt_board_list:[1,4,1,""],crawl_ptt_post:[1,4,1,""],crawl_wiki_entity:[1,4,1,""]},"eyes.celery.crawler.tasks.CrawlerTask":{after_return:[1,2,1,""],sess:[1,3,1,""]},"eyes.celery.ml":{tasks:[1,0,0,"-"]},"eyes.celery.ml.tasks":{MlTask:[1,1,1,""],transform_ptt_post_to_spacy_post:[1,4,1,""]},"eyes.celery.ml.tasks.MlTask":{nlp:[1,3,1,""],sess:[1,3,1,""]},"eyes.celery.stats":{tasks:[1,0,0,"-"]},"eyes.celery.stats.tasks":{StatsTask:[1,1,1,""],ptt_monthly_summary:[1,4,1,""],stats_entity_summary:[1,4,1,""]},"eyes.celery.stats.tasks.StatsTask":{after_return:[1,2,1,""],nlp:[1,3,1,""],sess:[1,3,1,""]},"eyes.config":{CeleryConfig:[2,1,1,""],EyesConfig:[2,1,1,""],MySQLConfig:[2,1,1,""],SpacyConfig:[2,1,1,""]},"eyes.config.CeleryConfig":{broker_url:[2,5,1,""],installed_apps:[2,5,1,""],result_backend:[2,5,1,""],result_backend_transport_options:[2,5,1,""],task_serializer:[2,5,1,""],timezone:[2,5,1,""]},"eyes.config.EyesConfig":{from_yaml:[2,2,1,""]},"eyes.config.MySQLConfig":{database:[2,5,1,""],host:[2,5,1,""],password:[2,5,1,""],port:[2,5,1,""],user:[2,5,1,""]},"eyes.config.SpacyConfig":{name:[2,5,1,""]},"eyes.crawler":{dcard:[3,0,0,"-"],entity:[3,0,0,"-"],ptt:[3,0,0,"-"],utils:[3,0,0,"-"]},"eyes.crawler.dcard":{crawl_board_list:[3,6,1,""],crawl_post:[3,6,1,""],crawl_post_ids:[3,6,1,""]},"eyes.crawler.entity":{crawl_wiki_entity:[3,6,1,""],crawl_wiki_entity_urls:[3,6,1,""]},"eyes.crawler.ptt":{crawl_board_list:[3,6,1,""],crawl_post:[3,6,1,""],crawl_post_urls:[3,6,1,""],get_next_url:[3,6,1,""],get_post_id:[3,6,1,""]},"eyes.crawler.utils":{get_dom:[3,6,1,""]},"eyes.data":{Board:[4,1,1,""],Comment:[4,1,1,""],Entity:[4,1,1,""],Post:[4,1,1,""],dcard:[4,0,0,"-"],ptt:[4,0,0,"-"],spacy:[4,0,0,"-"],stats:[4,0,0,"-"]},"eyes.data.Board":{name:[4,5,1,""]},"eyes.data.Comment":{created_at:[4,5,1,""],updated_at:[4,5,1,""]},"eyes.data.Entity":{alias:[4,5,1,""],label:[4,5,1,""],name:[4,5,1,""],to_wiki_entity_orm:[4,2,1,""],type:[4,5,1,""]},"eyes.data.Post":{created_at:[4,5,1,""],updated_at:[4,5,1,""]},"eyes.data.dcard":{DcardBoard:[4,1,1,""],DcardComment:[4,1,1,""],DcardPost:[4,1,1,""],DcardReaction:[4,1,1,""]},"eyes.data.dcard.DcardBoard":{alias:[4,5,1,""],created_at:[4,5,1,""],description:[4,5,1,""],id:[4,5,1,""],is_school:[4,5,1,""],to_orm:[4,2,1,""],updated_at:[4,5,1,""]},"eyes.data.dcard.DcardComment":{to_orm:[4,2,1,""]},"eyes.data.dcard.DcardPost":{to_orm:[4,2,1,""]},"eyes.data.dcard.DcardReaction":{to_orm:[4,2,1,""]},"eyes.data.ptt":{PttBoard:[4,1,1,""],PttComment:[4,1,1,""],PttPost:[4,1,1,""]},"eyes.data.ptt.PttBoard":{to_orm:[4,2,1,""],url:[4,5,1,""]},"eyes.data.ptt.PttComment":{author:[4,5,1,""],comment_id:[4,5,1,""],content:[4,5,1,""],post_id:[4,5,1,""],reaction:[4,5,1,""],to_orm:[4,2,1,""]},"eyes.data.ptt.PttPost":{author:[4,5,1,""],board:[4,5,1,""],comments:[4,5,1,""],content:[4,5,1,""],id:[4,5,1,""],title:[4,5,1,""],to_orm:[4,2,1,""],url:[4,5,1,""]},"eyes.data.spacy":{SpacyPttComment:[4,1,1,""],SpacyPttPost:[4,1,1,""]},"eyes.data.spacy.SpacyPttComment":{to_orm:[4,2,1,""]},"eyes.data.spacy.SpacyPttPost":{to_orm:[4,2,1,""]},"eyes.data.stats":{DailySummary:[4,1,1,""],EntitySummary:[4,1,1,""],MonthlySummary:[4,1,1,""]},"eyes.data.stats.DailySummary":{to_orm:[4,2,1,""]},"eyes.data.stats.EntitySummary":{Config:[4,1,1,""],to_orm:[4,2,1,""]},"eyes.data.stats.MonthlySummary":{to_orm:[4,2,1,""]},"eyes.db":{dcard:[5,0,0,"-"],ptt:[5,0,0,"-"],spacy:[5,0,0,"-"],stats:[5,0,0,"-"],wiki:[5,0,0,"-"]},"eyes.db.dcard":{DcardBoard:[5,1,1,""],DcardComment:[5,1,1,""],DcardPost:[5,1,1,""],DcardReaction:[5,1,1,""]},"eyes.db.ptt":{PttBoard:[5,1,1,""],PttComment:[5,1,1,""],PttPost:[5,1,1,""]},"eyes.db.spacy":{SpacyPttComment:[5,1,1,""],SpacyPttPost:[5,1,1,""]},"eyes.db.stats":{DailySummary:[5,1,1,""],EntitySummary:[5,1,1,""],MonthlySummary:[5,1,1,""]},"eyes.db.wiki":{WikiEntity:[5,1,1,""]},"eyes.exception":{InvalidFormatError:[6,7,1,""],PostNotExistsError:[6,7,1,""]},"eyes.job":{JobType:[7,1,1,""],Jobs:[7,1,1,""]},"eyes.job.Jobs":{crawl_dcard_board_list:[7,2,1,""],crawl_dcard_latest_posts:[7,2,1,""],crawl_ptt_board_list:[7,2,1,""],crawl_ptt_latest_posts:[7,2,1,""],crawl_ptt_top_board_posts:[7,2,1,""],crawl_wiki_entities:[7,2,1,""],dispatch:[7,2,1,""],entity_monthly_summary:[7,2,1,""],job_map:[7,3,1,""],ptt_monthly_summary:[7,2,1,""],ptt_spacy_pipeline:[7,2,1,""]},"eyes.ml":{lf:[8,0,0,"-"],spacy:[8,0,0,"-"]},"eyes.ml.lf":{NERAnnotator:[8,1,1,""],build_tries:[8,6,1,""]},"eyes.ml.lf.NERAnnotator":{add_all:[8,2,1,""],add_gazetteers:[8,2,1,""]},"eyes.ml.spacy":{binary_to_doc:[8,6,1,""],build_docs:[8,6,1,""],transform_ptt_comment:[8,6,1,""],transform_ptt_post:[8,6,1,""],transform_ptt_post_to_spacy:[8,6,1,""]},"eyes.schema":{DailySummary:[9,1,1,""],DictType:[9,1,1,""],EntitySummary:[9,1,1,""],MonthSummary:[9,1,1,""],PttComment:[9,1,1,""],PttPost:[9,1,1,""],Query:[9,1,1,""],WikiEntity:[9,1,1,""]},"eyes.schema.DictType":{parse_literal:[9,2,1,""],parse_value:[9,2,1,""],serialize:[9,2,1,""]},"eyes.schema.EntitySummary":{connection:[9,5,1,""]},"eyes.schema.PttComment":{connection:[9,5,1,""]},"eyes.schema.PttPost":{connection:[9,5,1,""]},"eyes.schema.Query":{resolve_all_stats_entity_summaries:[9,2,1,""],resolve_daily_summaries:[9,2,1,""],resolve_entity_summary:[9,2,1,""],resolve_monthly_summaries:[9,2,1,""],resolve_monthly_summary:[9,2,1,""]},"eyes.schema.WikiEntity":{connection:[9,5,1,""]},eyes:{celery:[1,0,0,"-"],config:[2,0,0,"-"],data:[4,0,0,"-"],exception:[6,0,0,"-"],job:[7,0,0,"-"],ml:[8,0,0,"-"],schema:[9,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","property","Python property"],"4":["py","task","task"],"5":["py","attribute","Python attribute"],"6":["py","function","Python function"],"7":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:property","4":"py:task","5":"py:attribute","6":"py:function","7":"py:exception"},terms:{"100000":8,"32":8,"3306":2,"3600":2,"404":3,"byte":[4,8],"class":[1,2,4,5,7,8,9],"default":10,"final":10,"function":8,"int":[1,2,3,4,8,9],"public":0,"return":[1,3,4,7,8,9],"static":9,A:11,If:3,_env_fil:2,_env_file_encod:2,_secrets_dir:2,add:[8,10],add_al:8,add_gazett:8,admin:10,after:[1,10],after_return:1,alia:[4,9],all:[8,9],also:10,an:10,annot:8,anonym:4,anonymous_depart:4,anonymous_school:4,api:10,app:[1,2],ar:3,arg:[1,9,11],argoproj:10,asia:2,author:4,backend:2,base:[1,4,9],batch_siz:8,befor:11,binari:8,binary_to_doc:8,bind:10,bitnami:10,board:[1,3,4,5,7,11],board_stat:4,bool:4,broker:2,broker_url:2,build:8,build_doc:8,build_tri:8,callabl:7,callback:1,categori:3,category_url:3,celeri:[0,2,10,11],celeryconfig:2,cfg:12,chart:10,classmethod:2,cluster:10,clusterrol:10,command:10,comment:[4,5,8,9],comment_id:4,config:[0,4,10,12],configmap:10,connect:9,consum:11,contain:[3,4],content:4,count:4,crawl:[1,3,7,11],crawl_board_list:3,crawl_dcard_board_list:[1,7,11],crawl_dcard_latest_post:[7,11],crawl_dcard_post:1,crawl_post:3,crawl_post_id:3,crawl_post_url:3,crawl_ptt_board_list:[1,7,11],crawl_ptt_latest_post:[7,11],crawl_ptt_post:1,crawl_ptt_top_board_post:[7,11],crawl_wiki_ent:[1,3,7,11],crawl_wiki_entity_url:3,crawler:[0,2,6,7],crawlertask:1,creat:[2,3,4],created_at:4,cron:10,current:3,dai:[3,4,11],daili:[4,5,9],dailysummari:[4,5,9],data:[0,3,8],databas:[1,2],datetim:4,db:[0,4,8,10],dcard:[0,1,7],dcardboard:[3,4,5],dcardcom:[4,5],dcardpost:[3,4,5],dcardreact:[4,5],decod:8,definit:9,descript:4,dev:12,dev_fil:12,dict:[1,2,4,7,8,9],dictionari:[1,8],dicttyp:9,disabl:8,dispatch:[7,11],doc:[7,8],document:8,dom:3,dt:9,element:3,entiti:[1,4,5,7,8,9],entity_monthly_summari:7,entitysummari:[4,5,9],entitysummaryconnect:9,etl:10,etre:3,except:0,exist:6,ey:[10,11],eyesconfig:2,eyew:10,f:10,famou:10,file:2,finish:1,first:[10,11],floor:4,focus:0,format:6,forum:[0,3,4,11],forum_id:[3,4,11],forum_nam:4,from:[2,7],from_yaml:2,gazett:8,gender:4,get:3,get_dom:3,get_next_url:3,get_post_id:3,github:10,graphen:9,graphql:9,helm:10,host:[2,4,10],http:10,id:[1,3,4,11],ignor:3,index:0,info:9,init:10,initi:12,instal:[0,2],installed_app:2,invalid:6,invalidformaterror:6,io:10,is_school:4,iter:[3,8],job:[0,1,10],job_map:7,job_typ:11,jobtyp:7,json:2,kubectl:10,kwarg:[1,5,9],label:[1,3,4,8],languag:[1,8],last:9,latest:[3,7,11],like_count:4,limit:[1,8,9],line:10,link_stat:4,list:[1,2,3,4,7,8,9,11],liter:9,lxml:3,mainli:10,manag:10,map:7,max:[3,8,9],media:4,method:9,min_count:9,mine:0,ml:[0,2,7,11],mltask:1,model:[0,1,2,3,4,5,8],modul:[0,1,2,3,4,5,6,7,8,9],month:[1,4,9,11],monthli:[1,4,5,9],monthlysummari:[4,5,9],monthsummari:9,mysql:[2,10],mysqlconfig:2,n:[1,3,10,11],n_dai:[3,11],name:[1,2,3,4,9,11],need:10,ner:8,nerannot:8,next:3,nlp:[1,8],node:9,none:[1,2,3,4],nonetyp:1,ns:10,number:[3,8,9],object:2,onli:11,opinion:0,option:[1,2,3,4],orm:[4,5,8],our:10,output:12,output_dir:12,overwrit:11,page:[0,3],paramet:[1,2,3,7,8,9],pars:9,parse_liter:9,parse_valu:9,password:2,path:[2,12],pathlib:2,pipelin:8,port:[2,10],post:[1,3,4,5,6,7,8,9,11],post_id:[1,3,4],postnotexistserror:6,properti:[1,7],ptt:[0,1,7,8,9],ptt_monthly_summari:[1,7,11],ptt_spacy_pipelin:[7,11],pttboard:[3,4,5],pttcomment:[4,5,9],pttcommentconnect:9,pttpost:[3,4,5,8,9],pttpostconnect:9,pydant:4,queri:9,rang:3,reaction:[4,5],reaction_id:4,redi:10,relai:9,rememb:[10,11],repo:10,repositori:[10,11],request:3,resolv:9,resolve_all_stats_entity_summari:9,resolve_daily_summari:9,resolve_entity_summari:9,resolve_monthly_summari:9,resp:3,respons:3,result:2,result_backend:2,result_backend_transport_opt:2,role:10,rolebind:10,row:11,run:[7,11],schema:0,school:4,search:0,second:10,send:0,serial:[2,9],serviceaccount:10,sess:[1,8],session:[1,8],set:3,sever:10,skweak:8,sourc:[4,9],sourcetyp:4,spaci:[1,2,7,12],spacyconfig:2,spacypttcom:[4,5,8],spacypttpost:[4,5,8],sqlalchemi:[1,8],start:11,stat:[2,7,9,11],statist:7,stats_entity_summari:1,statstask:1,store:1,str:[1,2,3,4,8,9],string:8,summari:[1,4,5,7,9],system:0,tabl:10,taipei:2,taiwanes:0,task:2,task_seri:2,thi:[3,4,11],time:4,timezon:2,titl:4,to_orm:4,to_wiki_entity_orm:4,tok2vec:8,token:8,tool:10,top:[1,3,7,11],top_n:[1,3,11],topic:4,total_com:4,total_post:4,train:0,train_fil:12,transform:[1,3,4,7,8],transform_ptt_com:8,transform_ptt_post:8,transform_ptt_post_to_spaci:8,transform_ptt_post_to_spacy_post:1,transport:2,tri:8,trie:8,type:[1,2,3,4,7,8,9],union:[1,2],updat:[4,10],updated_at:4,url:[1,2,3,4],us:[8,10],user:[2,10],usernam:2,valu:[7,9,10],vector:12,visibility_timeout:2,we:10,web:10,whether:[4,11],which:3,wide:10,wiki:[1,2,3,4,9],wikient:[4,5,9],wikientityconnect:9,wikipedia:7,wip:10,with_nicknam:4,worker:[10,11],yaml:[2,10],year:[1,4,9,11],you:[10,11],zh_core_web_md:12,zh_core_web_sm:2},titles:["Eyes","eyes.celery","eyes.config","eyes.crawler","eyes.data","eyes.db","eyes.exception","eyes.job","eyes.ml","eyes.schema","Installation","Send jobs","Train models"],titleterms:{api:0,argo:10,built:12,celeri:1,command:11,compos:10,config:2,crawler:[1,3],creat:10,data:4,databas:10,db:5,dcard:[3,4,5],deploi:10,docker:10,document:0,entiti:3,except:6,ey:[0,1,2,3,4,5,6,7,8,9],guid:0,indic:0,initi:10,instal:10,job:[7,11],kubernet:10,lf:8,ml:[1,8],model:12,namespac:10,ptt:[3,4,5],recommend:10,schema:9,send:11,servic:10,spaci:[4,5,8],stat:[1,4,5],tabl:0,task:1,train:12,user:0,util:3,wiki:5,workflow:10,zh_core_eyes_md:12}})