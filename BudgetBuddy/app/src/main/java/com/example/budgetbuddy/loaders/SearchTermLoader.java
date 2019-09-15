package com.example.budgetbuddy.loaders;

import android.content.Context;

import androidx.annotation.Nullable;

import com.example.budgetbuddy.model.MerchantSummary;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by waltermao on 2018-03-31.
 */

public class SearchTermLoader extends BaseLoader<List<MerchantSummary>> {

    private String mSearchTerm;

    public SearchTermLoader(Context context, String searchTerm) {
        super(context);
        mSearchTerm = searchTerm;
    }

    @Nullable
    @Override
    public List<MerchantSummary> loadInBackground() {
        return new ArrayList<>(); // TODO
    }
}
