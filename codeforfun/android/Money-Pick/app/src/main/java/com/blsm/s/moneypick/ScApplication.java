package com.blsm.s.moneypick;

import android.app.Application;

import com.blsm.s.moneypick.http.VolleyNetCenter;

/**
 * Created by ScorpiusZjj on 12/23/14.
 */
public class ScApplication extends Application{

    @Override
    public void onCreate() {
        super.onCreate();

        VolleyNetCenter.init(this);

    }
}
