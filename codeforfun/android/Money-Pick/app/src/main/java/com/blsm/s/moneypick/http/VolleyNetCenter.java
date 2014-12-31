package com.blsm.s.moneypick.http;

import android.content.Context;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

/**
 * Created by ScorpiusZjj on 12/29/14.
 */
public class VolleyNetCenter {

    private static RequestQueue mRequestQueue;

    public static void init(Context context){
        mRequestQueue= Volley.newRequestQueue(context.getApplicationContext());
    }

    public static RequestQueue getmRequestQueue(){
        if (null != mRequestQueue){
            return mRequestQueue;
        }else {
            throw new IllegalStateException("RequestQueue not initialized");
        }
    }

}
