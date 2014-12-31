package com.blsm.s.moneypick.receiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

import com.blsm.s.moneypick.ScreenLockActivity_;
import com.blsm.s.moneypick.utils.ScLog;

/**
 * Created by ScorpiusZjj on 12/23/14.
 */
public class ScreenLockReceiver extends BroadcastReceiver{

    private static final String TAG = ScreenLockReceiver.class.getSimpleName();

    @Override
    public void onReceive(Context context, Intent intent) {
        ScLog.i(TAG,"onReceive");
        if (null == intent)
            return;
        String action=intent.getAction();
        ScLog.i(TAG,"onReceive :: action = "+action);
        if (Intent.ACTION_SCREEN_OFF.equals(action)){
            ScreenLockActivity_.intent(context).flags(Intent.FLAG_ACTIVITY_NEW_TASK).start();
        }
    }
}
