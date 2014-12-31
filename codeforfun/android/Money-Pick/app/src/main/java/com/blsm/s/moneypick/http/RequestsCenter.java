package com.blsm.s.moneypick.http;

import android.text.TextUtils;

import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.blsm.s.moneypick.utils.NetworkUtil;
import com.blsm.s.moneypick.utils.ScLog;

import org.apache.http.protocol.HTTP;

import java.io.UnsupportedEncodingException;
import java.lang.ref.WeakReference;
import java.util.Map;

/**
 * Created by ScorpiusZjj on 12/29/14.
 */
public class RequestsCenter {

    private static final String TAG = RequestsCenter.class.getSimpleName();


    public static void doDeleteRequest(String url,Map<String , String> headers,Map<String
            , String> params,String data,RequestsCallback requestsCallback){
        doRequest(Request.Method.DELETE,url,headers,params,data,requestsCallback);
    }

    public static void doPutRequest(String url,Map<String , String> headers,Map<String
            , String> params,String data,RequestsCallback requestsCallback){
        doRequest(Request.Method.PUT,url,headers,params,data,requestsCallback);
    }

    public static void doGetRequest(String url,Map<String
            , String> params,RequestsCallback requestsCallback){
        doRequest(Request.Method.GET,url,null,params,"",requestsCallback);
    }

    public static void doGetRequest(String url,Map<String , String> headers,Map<String
            , String> params,String data,RequestsCallback requestsCallback){
        doRequest(Request.Method.GET,url,headers,params,data,requestsCallback);
    }

    public static void doPostRequest(String url,Map<String , String> headers,Map<String
            , String> params,String data,RequestsCallback requestsCallback){
        doRequest(Request.Method.POST, url, headers, params, data, requestsCallback);
    }

    private static void doRequest(int method,String url,Map<String , String> headers,Map<String
            , String> params,String data, RequestsCallback requestsCallback){

        if(!NetworkUtil.isConnected()){
            return;
        }

        final WeakReference<RequestsCallback> mRequestsCallbackWeakReference=
                new WeakReference<RequestsCallback>(requestsCallback);
        VoRequest request = new VoRequest(method, url, new Response.Listener<NetworkResponse>() {
            @Override
            public void onResponse(NetworkResponse response) {
                doResponse(response, mRequestsCallbackWeakReference);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                if(null != error.networkResponse)
                    doResponse(error.networkResponse, mRequestsCallbackWeakReference);
                else
                    doResponse(null,mRequestsCallbackWeakReference);
            }
        });


        updateRequest(request,method,headers,params,data);


        VolleyNetCenter.getmRequestQueue().add(request);
    }

    private static void updateRequest(VoRequest request, int method,  Map<String, String> headers
            , Map<String, String> params, String data) {

        if (Request.Method.GET == method)
            request.setShouldCache(true);
        if (null != headers && headers.size()>0)
            request.setHeaders(headers);
        if (null != params && params.size()>0)
            request.setParams(params);
        if(null != data&& !TextUtils.isEmpty(data))
            request.setBody(data);
        if (method == Request.Method.POST
                || method == Request.Method.PUT ){
            request.setBodyContentType("application/json");
        }


    }

    private static void doResponse(NetworkResponse response, WeakReference<RequestsCallback> mRequestsCallbackWeakReference) {
        ScLog.i(TAG,"doResponse :: response = "+response);
        boolean isSuccess=false;
        String msg="";

        // deal with response
        //failed
        if (null == response){
            msg="未知错误";
        }
        else {
            String result=parseResponse(response.data);
            isSuccess=isSuccessByStatusCode(response.statusCode);
            msg=result;
            ScLog.i(TAG,"doResponse :: status_code = "+response.statusCode
                    + " networkTimeMs = "+response.networkTimeMs
                    + " notModified = "+response.notModified
                    + " data = "+result);
        }

        // Callback
        try {
            RequestsCallback listener = mRequestsCallbackWeakReference.get();
            if (listener == null) {
                return;
            }
            if (listener instanceof android.support.v4.app.Fragment) {
                android.support.v4.app.Fragment fragment = (android.support.v4.app.Fragment) listener;
                if (fragment.isAdded()) {
                    listener.onRequestFinished(isSuccess,msg);
                }
            } else {
                listener.onRequestFinished(isSuccess,msg);
            }
        } catch (Exception e) {
            ScLog.d(TAG, "doResponse :: Callback Error = " + e.getMessage());
            e.printStackTrace();
        }

    }

    private static boolean isSuccessByStatusCode(int statusCode) {
        if (statusCode >= 200 && statusCode <400){
            return true;
        }else {
            return false;
        }
    }

    private static String parseResponse(byte[] data) {
        if (null != data && data.length>0){
            try {
                return new String(data, HTTP.UTF_8);
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
                ScLog.w(TAG,e.getMessage());
                return "";
            }
        }else {
            ScLog.w(TAG,"parseResponse :: data is null");
            return "";
        }
    }

}
