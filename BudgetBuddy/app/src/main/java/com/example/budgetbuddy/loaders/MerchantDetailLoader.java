package com.example.budgetbuddy.loaders;

import android.content.Context;

import androidx.annotation.Nullable;

import com.example.budgetbuddy.model.Merchant;
import com.example.budgetbuddy.utils.NetworkUtils;

import org.json.JSONException;
import org.json.JSONObject;

public class MerchantDetailLoader extends BaseLoader<Merchant>{

    private String mMerchantName;
    private double mLatitude;
    private double mLongitude;

    public MerchantDetailLoader(Context context, String merchantName, double latitude, double longitude) {
        super(context);
        mMerchantName = merchantName;
        mLatitude = latitude;
        mLongitude = longitude;
    }

    @Nullable
    @Override
    public Merchant loadInBackground() {
        if (!NetworkUtils.isNetworkAvailable(getContext())) {
            return null;
        }
        String requestUrl = NetworkUtils.MERCHANT_DETAILS_URL;
        JSONObject response = null;
        try{
            JSONObject requestJSON = new JSONObject();
            requestJSON.put("merchantName", mMerchantName);
            requestJSON.put("latitude", mLatitude);
            requestJSON.put("longitude", mLongitude);
            requestJSON.put("dayRange", MerchantSummaryLoader.DAYS_IN_PAST);

            String responseString = NetworkUtils.executeRequest(requestUrl, requestJSON);
            if (responseString == null || responseString.isEmpty()) {
                return null;
            }
            response = new JSONObject(responseString);
            Merchant merchant = new Merchant(
                    mMerchantName,
                    response.getString("address"),
                    response.getString("city"),
                    response.getDouble("distance"),
                    response.getDouble("averageSpending"),
                    response.getDouble("medianSpending"),
                    response.getInt("transactionCount")
            );
            return merchant;
        } catch(JSONException e) {
            e.printStackTrace();
            return null;
        }
    }
}
