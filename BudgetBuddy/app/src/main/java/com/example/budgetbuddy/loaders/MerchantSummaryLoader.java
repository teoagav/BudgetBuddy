package com.example.budgetbuddy.loaders;

import android.content.Context;

import androidx.annotation.Nullable;

import com.example.budgetbuddy.model.MerchantSummary;
import com.example.budgetbuddy.utils.NetworkUtils;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class MerchantSummaryLoader extends BaseLoader<List<MerchantSummary>>{

    public static final int DAYS_IN_PAST = 92;
    private double mLatitude;
    private double mLongitude;

    public MerchantSummaryLoader(Context context, double latitude, double longitude) {
        super(context);
        mLatitude = latitude;
        mLongitude = longitude;
    }

    @Nullable
    @Override
    public List<MerchantSummary> loadInBackground() {
        if (!NetworkUtils.isNetworkAvailable(getContext())) {
            return new ArrayList<>();
        }
        String requestUrl = NetworkUtils.MERCHANT_LIST_URL;

        JSONObject response = null;
        try{
            JSONObject requestJSON = new JSONObject();
            requestJSON.put("latitude", mLatitude);
            requestJSON.put("longitude", mLongitude);
            requestJSON.put("dayRange", DAYS_IN_PAST);
            String responseString = NetworkUtils.executeRequest(requestUrl, requestJSON);
            if (responseString == null || responseString.isEmpty()) {
                return new ArrayList<>();
            }
            response = new JSONObject(responseString);

            List<MerchantSummary> merchantSummaries = new ArrayList<>();
            JSONArray arr = response.getJSONArray("merchants");
            for (int i = 0; i < arr.length(); ++i) {
                JSONObject obj = arr.getJSONObject(i);
                MerchantSummary summary = new MerchantSummary(obj.getString("name"),
                        obj.getDouble("averageSpending"),
                        obj.getInt("distance"),
                        mLatitude,
                        mLongitude);
                merchantSummaries.add(summary);
            }
            return merchantSummaries;
        } catch(JSONException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }
}
