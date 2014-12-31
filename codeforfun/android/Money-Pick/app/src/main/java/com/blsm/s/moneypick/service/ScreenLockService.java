package com.blsm.s.moneypick.service;

import android.app.Service;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.IBinder;

import com.blsm.s.moneypick.utils.ScLog;
import com.blsm.s.moneypick.receiver.ScreenLockReceiver;

import org.androidannotations.annotations.EService;

/**
 * Created by ScorpiusZjj on 12/23/14.
 */
@EService
public class ScreenLockService extends Service{

    private static final String TAG = ScreenLockService.class.getSimpleName();
    private ScreenLockReceiver receiver;

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onCreate() {
        ScLog.i(TAG,"onCreate ::");
        super.onCreate();
        registe();
    }

    private void registe() {
        if (null == receiver){
            receiver=new ScreenLockReceiver();
        }
        IntentFilter filter=new IntentFilter();
        filter.addAction(Intent.ACTION_SCREEN_ON);
        filter.addAction(Intent.ACTION_SCREEN_OFF);
        filter.setPriority(999);
        registerReceiver(receiver,filter);
    }

    @Override
    public void onDestroy() {
        ScLog.i(TAG,"onDestroy ::");
        super.onDestroy();
        unRegiste();
    }

    private void unRegiste() {
        if (null != receiver)
            unregisterReceiver(receiver);
    }
}
