package com.example.budgetbuddy.model;

import android.os.Parcel;
import android.os.Parcelable;

import java.text.DecimalFormat;

public class Merchant implements Parcelable {

    private String mName;
    private String mAddress;
    private String mCity;
    private double mDistance;
    private double mAverageSpending;
    private double mMedianSpending;
    private int mTransactionCount;

    public Merchant(String name, String address, String city, double distance, double averageSpending, double medianSpending, int transactionCount) {
        mName = name;
        mAddress = address;
        mCity = city;
        mDistance = distance;
        mAverageSpending = averageSpending;
        mMedianSpending = medianSpending;
        mTransactionCount = transactionCount;
    }

    public String getName() {
        return mName;
    }

    public String getAddress() {
        return mAddress;
    }

    public String getCity() {
        return mCity;
    }

    public String getDistance() {
        DecimalFormat twoDForm = new DecimalFormat("#.##");
        return twoDForm.format(mDistance) + " meters away";
    }

    public String getAverageSpending() {
        DecimalFormat twoDForm = new DecimalFormat("#.##");
        return "Average spending: " + twoDForm.format(mAverageSpending);
    }

    public String getMedianSpending() {
        DecimalFormat twoDForm = new DecimalFormat("#.##");
        return "Median spending: " + twoDForm.format(mMedianSpending);
    }

    public int getTransactionCount() {
        return mTransactionCount;
    }

    public static final Creator<Merchant> CREATOR = new Creator<Merchant>() {
        @Override
        public Merchant createFromParcel(Parcel in) {
            return new Merchant(in);
        }

        @Override
        public Merchant[] newArray(int size) {
            return new Merchant[size];
        }
    };

    @Override
    public int describeContents() {
        return 0;
    }

    protected Merchant(Parcel in) {
        mName = in.readString();
        mAddress = in.readString();
        mCity = in.readString();
        mDistance = in.readDouble();
        mAverageSpending = in.readDouble();
        mMedianSpending = in.readDouble();
        mTransactionCount = in.readInt();
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(mName);
        dest.writeString(mAddress);
        dest.writeString(mCity);
        dest.writeDouble(mDistance);
        dest.writeDouble(mAverageSpending);
        dest.writeDouble(mMedianSpending);
        dest.writeInt(mTransactionCount);
    }
}
