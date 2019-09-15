package com.example.budgetbuddy.utils;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * This class exists because:
 * 1. need to pass in a string as a key value
 * 2. Key values need to implement Parcelable
 * 3. String doesn't implement parcelable :(
 */
public class ParcelableString implements Parcelable {
    private String mString;

    public ParcelableString(String str) {
        mString = str;
    }

    public String getString() {
        return mString;
    }

    /////////////////////////////////// PARCELABLE ///////////////////////////////

    protected ParcelableString(Parcel in) {
        mString = in.readString();
    }

    public static final Creator<ParcelableString> CREATOR = new Creator<ParcelableString>() {
        @Override
        public ParcelableString createFromParcel(Parcel in) {
            return new ParcelableString(in);
        }

        @Override
        public ParcelableString[] newArray(int size) {
            return new ParcelableString[size];
        }
    };

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel parcel, int i) {
        parcel.writeString(mString);
    }
}
