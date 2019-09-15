package com.example.budgetbuddy.loaders;

import android.content.Context;
import android.location.Location;

import androidx.annotation.Nullable;

public class LocationLoader extends BaseLoader<Location> {

    public LocationLoader(Context context) {
        super(context);
    }

    @Nullable
    @Override
    public Location loadInBackground() {
        return null;
    }
}
