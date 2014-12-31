package com.blsm.s.moneypick;

import android.view.WindowManager;
import android.widget.TextView;

import com.blsm.s.moneypick.base.BaseActivity;

import org.androidannotations.annotations.AfterViews;
import org.androidannotations.annotations.Click;
import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.ViewById;

/**
 * Created by ScorpiusZjj on 12/23/14.
 */
@EActivity(R.layout.activity_screen_lock)
public class ScreenLockActivity extends BaseActivity{

    @ViewById(R.id.lable)
    TextView lable;

    @AfterViews
    void init(){
        addRequireFlags();
        lable.setText("hahahah");
    }

    private void addRequireFlags() {
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON
                |WindowManager.LayoutParams.FLAG_DISMISS_KEYGUARD
                |WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED);
    }

    @Click(R.id.stop)
    void stop(){
        finish();
    }
}
