package com.blsm.s.moneypick;

import android.widget.TextView;

import com.blsm.s.moneypick.base.BaseActivity;
import com.blsm.s.moneypick.constant.Actions;
import com.blsm.s.moneypick.service.ScreenLockService_;

import org.androidannotations.annotations.AfterViews;
import org.androidannotations.annotations.Click;
import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.ViewById;

/**
 * Created by ScorpiusZjj on 12/23/14.
 */
@EActivity(R.layout.activity_main)
public class MainActivity extends BaseActivity{

    private static final String TAG = MainActivity.class.getSimpleName();

    @ViewById
    TextView navi_title;

    @AfterViews
    void init(){
        navi_title.setText(this.getClass().getSimpleName());
    }

    @Click(R.id.button)
    void serviceStart(){
        ScreenLockService_.intent(this).action(Actions.LOCK_SCREEN_SERVICE_INIT).start();
    }

    @Click(R.id.network)
    void gotoNetworkTest(){
        NetWorkActivity_.intent(this).start();
    }

}
