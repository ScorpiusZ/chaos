package com.blsm.s.moneypick.receiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

import com.blsm.s.moneypick.constant.Actions;
import com.blsm.s.moneypick.service.ScreenLockService;

import org.androidannotations.annotations.EReceiver;
import org.androidannotations.annotations.ReceiverAction;

/**
 * Created by ScorpiusZjj on 12/24/14.
 */
@EReceiver
public class MonitorReceiver extends BroadcastReceiver {

    @ReceiverAction(Intent.ACTION_USER_PRESENT)
    void doAction(Context context){
        wakeUpService(context);
    }


    private void wakeUpService(Context context){
        Intent wakeup=new Intent(context, ScreenLockService.class);
        wakeup.setAction(Actions.LOCK_SCREEN_SERVICE_INIT);
        context.startService(wakeup);
    }

    @Override
    public void onReceive(Context context, Intent intent) {

    }
}
