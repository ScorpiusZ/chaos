package com.blsm.s.moneypick;

import com.blsm.s.moneypick.utils.ScLog;
import com.blsm.s.moneypick.base.BaseActivity;
import com.blsm.s.moneypick.constant.Actions;
import com.blsm.s.moneypick.service.ScreenLockService_;

import org.androidannotations.annotations.AfterViews;
import org.androidannotations.annotations.Click;
import org.androidannotations.annotations.EActivity;

/**
 * Created by ScorpiusZjj on 12/23/14.
 */
@EActivity(R.layout.activity_main)
public class MainActivity extends BaseActivity{

    private static final String TAG = MainActivity.class.getSimpleName();


    @AfterViews
    void init(){
    }

    @Click(R.id.button)
    void serviceStart(){
        ScLog.i(TAG,"service_start ::");
        ScreenLockService_.intent(this).action(Actions.LOCK_SCREEN_SERVICE_INIT).start();
    }

    @Click(R.id.network)
    void gotoNetworkTest(){
        NetWorkActivity_.intent(this).start();
    }

}
