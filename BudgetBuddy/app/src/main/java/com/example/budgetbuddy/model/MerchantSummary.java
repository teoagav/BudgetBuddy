package com.example.budgetbuddy.model;

import android.os.Parcel;
import android.os.Parcelable;

import java.text.DecimalFormat;

public class MerchantSummary implements Parcelable {
    private String mMerchantName;
    private double mMerchantAverageSpending;
    private double mDistance;
    private double mLatitude;
    private double mLongitude;

    public MerchantSummary(String merchantName, double merchantAverageSpending, double distance, double latitude, double longitude) {
        this.mMerchantName = merchantName;
        this.mMerchantAverageSpending = merchantAverageSpending;
        this.mDistance = distance;
        this.mLatitude = latitude;
        this.mLongitude = longitude;
    }

    public String getMerchantName() {
        return mMerchantName;
    }

    public double getMerchantAverageSpending() {
        return mMerchantAverageSpending;
    }

    public String getMerchantAverageSpendingString() {
        DecimalFormat twoDForm = new DecimalFormat("#.##");
        return "Average spending: $" + twoDForm.format(mMerchantAverageSpending);
    }

    public double getDistance() {
        return mDistance;
    }

    public String getDistanceString() {
        DecimalFormat twoDForm = new DecimalFormat("#.##");
        return twoDForm.format(mDistance) + " meters away";
    }

    public double getLatitude() {
        return mLatitude;
    }

    public double getLongitude() {
        return mLongitude;
    }

    //////////////////////////// PARCELABLE ////////////////////////////////
    protected MerchantSummary(Parcel in) {
        mMerchantName = in.readString();
        mMerchantAverageSpending = in.readDouble();
        mDistance = in.readDouble();
    }

    public static final Creator<MerchantSummary> CREATOR = new Creator<MerchantSummary>() {
        @Override
        public MerchantSummary createFromParcel(Parcel in) {
            return new MerchantSummary(in);
        }

        @Override
        public MerchantSummary[] newArray(int size) {
            return new MerchantSummary[size];
        }
    };

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(mMerchantName);
        dest.writeDouble(mMerchantAverageSpending);
        dest.writeDouble(mDistance);
    }
}
