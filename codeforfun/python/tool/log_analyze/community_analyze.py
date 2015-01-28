#! /usr/bin/env python
#coding:utf8
import data_analyze as da
import id_util

pr_format='{0},{1},{2},{3},{4}\n'

sum_pr_format='{0},{1},{2},{3}\n'

def community_summarize(datetime):
    global list_df,create_df,privateMsg_df
    result=''
    result+='private_message,'+str(len(privateMsg_df))+'\n\n'
    lists=da.rowGroupCount(list_df,'values')
    creates=da.rowGroupCount(create_df,'values')
    users=da.getUniqueDevice(datetime,'topic_list','values')
    result=result+sum_pr_format.format('node_id','node_pv','topic_create','user')
    for node_id in lists.keys():
        result=result+sum_pr_format.format(id_util.decode_node(node_id),lists[node_id],\
                creates.get(node_id,0),users.get(node_id,0))
    result=result+'sum\n'
    result=result+sum_pr_format.format(len(lists.keys()),sum(lists),sum(creates),sum(users))
    return result


def community_static(datetime):
    global like_df,follow_df,view_df,reply_df
    likes=da.rowGroupCount(like_df,'values')
    follows=da.rowGroupCount(follow_df,'values')
    views=da.rowGroupCount(view_df,'values')
    replies=da.rowGroupCount(reply_df,'values')
    result='\n'
    result=result+pr_format.format('topic_id','view_count','like','follow','reply')
    for topic_id in views.keys()[:50]:
        result=result+pr_format.format(id_util.decode_topic(topic_id),views.get(topic_id,0),likes.get(topic_id,0),\
                follows.get(topic_id,0),replies.get(topic_id,0))
    return result


def community_report(datetime):
    init(datetime)
    data=''
    data=data+community_summarize(datetime)
    data=data+community_static(datetime)
    da.write2CsvFile(datetime,'community',data)

def init(datetime):
    global list_df,like_df,follow_df,create_df,view_df,reply_df,privateMsg_df
    list_df,view_df,create_df,privateMsg_df,reply_df,like_df,follow_df=map(lambda x:da.getDataFrame(x,datetime),\
            ['topic_list','topic_view','topic_create','private_msg','reply','topic_like','topic_follow'])

def main():
    import sys
    date='20150105'
    if len(sys.argv) >1:
        date=sys.argv[1]
    community_report(date)


if __name__ == '__main__':
    main()
