package com.example.budgetbuddy.loaders;

import android.content.Context;

import androidx.loader.content.AsyncTaskLoader;

public abstract class BaseLoader<T> extends AsyncTaskLoader<T> {

    public BaseLoader(Context context) {
        super(context);
    }

    @Override
    protected void onStartLoading() {
        super.onStartLoading();
        forceLoad();
    }
}
