package com.blsm.s.moneypick;

import com.blsm.s.moneypick.utils.ScLog;
import com.blsm.s.moneypick.base.BaseActivity;
import com.blsm.s.moneypick.http.RequestsCallback;
import com.blsm.s.moneypick.http.RequestsCenter;

import org.androidannotations.annotations.AfterViews;
import org.androidannotations.annotations.Click;
import org.androidannotations.annotations.EActivity;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by ScorpiusZjj on 12/29/14.
 */
@EActivity(R.layout.activity_net)
public class NetWorkActivity extends BaseActivity implements RequestsCallback {

    private static final String TAG = NetWorkActivity.class.getSimpleName();

    @AfterViews
    void init(){
    }

    @Click
    void get(){
        ScLog.i(TAG,"get ::");
        Map<String , String> params=new HashMap<>();
        params.put("register_date","20141021");
        params.put("api_key","4def4d59");
        params.put("ver","1.3.7");
        Map<String ,String> headers=new HashMap<>();
        headers.put("api_key", "4def4d59");
//        RequestsCenter.doGetRequest( "http://api.aihuo360.com/v2/home" ,headers,params,"",this);
        RequestsCenter.doGetRequest( "http://api.aihuo360.com/v2/home" ,params,this);
    }

    @Click
    void post(){
        ScLog.i(TAG,"post :: ");
        Map<String ,String> headers=new HashMap<>();
        headers.put("apikey","4def4d59");
        String data="{\"body\": \"123qweasd\", \"sign\": \"454a259ef9c49c13ec6980fa68e40da1\", \"member\": {\"password\": \"785986\", \"id\": \"6ab01a6b59fceff880af71c89e1d4afc\"}, \"nickname\": \"blsm1234\", \"id\": \"3c0a886206c2cc2518837f2738d4449b\", \"device_id\": \"A000004800AE17\"}\n";
        RequestsCenter.doPostRequest("http://115.29.4.146:8080/v2/topics/3c0a886206c2cc2518837f2738d4449b/replies",
               headers,null,data,this);
    }

    @Click
    void put(){
        ScLog.i(TAG,"put :: ");
        Map<String ,String> headers=new HashMap<>();
        headers.put("apikey","4def4d59");
        String data="{\"sign\": \"2b002cad3e15ed07eeb8723e7ffa9653\", \"id\": \"69ec9facd9ba917014280b0b94426dbe\", \"device_id\": \"A000004800AE17\"}\n";
        RequestsCenter.doPutRequest("http://115.29.4.146:8080/v2/topics/69ec9facd9ba917014280b0b94426dbe/follow",headers,null,data,this);
    }

    @Click
    void delete(){
        ScLog.i(TAG,"delete :: ");
        Map<String ,String> headers=new HashMap<>();
        headers.put("apikey","4def4d59");
        Map<String ,String> params=new HashMap<>();
        params.put("id","69ec9facd9ba917014280b0b94426dbe");
        params.put("device_id","A000004800AE17");
        RequestsCenter.doDeleteRequest("http://115.29.4.146:8080/v2/topics/69ec9facd9ba917014280b0b94426dbe/unfollow", headers, params, "", this);
    }

    @Override
    public void onRequestFinished(boolean isSuccess, String msg) {
        ScLog.i(TAG,"onRequestFinished :: isSuccess = "+ isSuccess + " msg = "+msg);
    }
}
