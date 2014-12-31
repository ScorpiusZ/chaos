package com.blsm.s.moneypick.utils;

import android.util.Log;

/**
 * Created by ScorpiusZjj on 12/23/14.
 */
public class ScLog {
    private static boolean LogEnable=true;

    public static void v(String tag,String msg){
        if (LogEnable){
            try{
                Log.v(tag,msg );
            }catch (Exception e){

            }
        }
    }

    public static void d(String tag,String msg){
        if (LogEnable){
            try{
                Log.d(tag,msg );
            }catch (Exception e){

            }
        }
    }

    public static void i(String tag,String msg){
        if (LogEnable){
            try{
                Log.i(tag,msg );
            }catch (Exception e){

            }
        }
    }

    public static void w(String tag,String msg){
        if (LogEnable){
            try{
                Log.w(tag,msg );
            }catch (Exception e){

            }
        }
    }

    public static void e(String tag,String msg){
        if (LogEnable){
            try{
                Log.e(tag,msg );
            }catch (Exception e){

            }
        }
    }
}
