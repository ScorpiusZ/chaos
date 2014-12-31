package com.blsm.s.moneypick.http;

import android.text.TextUtils;

import com.blsm.s.moneypick.utils.ScLog;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.Map;

/**
 * Created by ScorpiusZjj on 12/29/14.
 */
public class HttpUtils {

    private static final String TAG = HttpUtils.class.getSimpleName();

    public static String genrateUrlparams(String url,
                                          Map<String, String> params, String charsetName) {

        if (TextUtils.isEmpty(url)) {
            ScLog.w(TAG, "genrateUrlparams :: url is empty");
            return "";
        }

        if (params == null || params.size() < 1) {
            ScLog.w(TAG, "genrateUrlparams :: params is empty");
            return "";
        }

        StringBuffer urlString = new StringBuffer("");
        if (url.contains("?")) {
            urlString = new StringBuffer("&");
        } else {
            urlString = new StringBuffer("?");
        }
        try {
            for (Map.Entry<String, String> param : params.entrySet()) {
                urlString.append(param.getKey() + "="
                        + URLEncoder.encode(param.getValue(), charsetName)
                        + "&");
            }
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            ScLog.e(TAG,
                    "genrateUrlparams :: UnsupportedEncodingException Erroe => "
                            + e.getMessage());
        }

        urlString = new StringBuffer(urlString.reverse().toString()
                .replaceFirst("&", ""));
        return urlString.reverse().toString();
    }

}
