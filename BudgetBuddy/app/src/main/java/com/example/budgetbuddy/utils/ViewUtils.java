package com.example.budgetbuddy.utils;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;

/**
 * Created by waltermao on 2018-04-01.
 */

public class ViewUtils {

    public static void hideSoftKeyboard(View view, Context context) {
        if (view != null && view.requestFocus()) {
            InputMethodManager imm = (InputMethodManager) context.getSystemService(Context.INPUT_METHOD_SERVICE);
            if (imm != null) {
                imm.hideSoftInputFromWindow(view.getWindowToken(), 0);
            }
        }
    }

    /**
     * Recursively set visibility of all views and child views
     *
     * @param view root view
     * @param show show or hide all views
     */
    public static void setViewsVisibility(View view, boolean show) {
        if (view instanceof ViewGroup) {
            ViewGroup viewGroup = (ViewGroup) view;
            for (int i = 0; i < viewGroup.getChildCount(); ++i) {
                View child = viewGroup.getChildAt(i);
                child.setEnabled(show);
                child.setVisibility(show ? View.VISIBLE : View.GONE);
                setViewsVisibility(child, show);
            }
        }
    }


}
