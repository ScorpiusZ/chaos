package com.blsm.s.moneypick.http;

import android.text.TextUtils;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.toolbox.HttpHeaderParser;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by ScorpiusZjj on 12/29/14.
 */
public class VoRequest extends Request<NetworkResponse>{

    private final Response.Listener<NetworkResponse> mListener;
    private Map<String, String> headers = new HashMap<String, String>();
    private Map<String, String> params = new HashMap<String, String>();
    private String bodyContentType;
    private String body;


    public VoRequest(int method, String url
            , Response.Listener<NetworkResponse> listener,Response.ErrorListener errorlistener) {
        super(method, url, errorlistener);
        mListener=listener;
    }

    @Override
    protected Response parseNetworkResponse(NetworkResponse response) {
        return Response.success(response, HttpHeaderParser.parseCacheHeaders(response));
    }

    @Override
    protected void deliverResponse(NetworkResponse response) {
        mListener.onResponse(response);
    }

    @Override
    public Map<String, String> getHeaders() {
        return headers;
    }

    @Override
    public byte[] getBody() throws AuthFailureError {
        if (!TextUtils.isEmpty(body)) {
            return body.getBytes();
        }
        return super.getBody();
    }

    @Override
    public String getBodyContentType() {
        if (!TextUtils.isEmpty(bodyContentType)) {
            return bodyContentType;
        }
        return super.getBodyContentType();
    }

    public void setHeaders(Map<String, String> headers) {
        this.headers = headers;
    }

    public void setParams(Map<String, String> params) {
        this.params = params;
    }

    public void setBodyContentType(String bodyContentType) {
        this.bodyContentType = bodyContentType;
    }

    public void setBody(String body) {
        this.body = body;
    }

    @Override
    public String getUrl() {
        if (null != params && params.size()>0){
            String originUlr=this.getOriginUrl();
            return originUlr+HttpUtils.genrateUrlparams(originUlr,params,getParamsEncoding());
        }
        else {
            return super.getUrl();
        }
    }
}
