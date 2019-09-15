package com.example.budgetbuddy.adapters;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;

import com.example.budgetbuddy.R;
import com.example.budgetbuddy.model.MerchantSummary;

import java.lang.ref.WeakReference;
import java.util.List;

public class MerchantsListAdapter extends BaseListAdapter<MerchantSummary> {

    private WeakReference<Context> mContextReference;

    public MerchantsListAdapter(List<MerchantSummary> data, Context context) {
        super(data);
        mContextReference = new WeakReference<>(context);
    }

    @NonNull
    @Override
    public MerchantViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        LayoutInflater inflater = LayoutInflater.from(mContextReference.get());
        return new MerchantViewHolder(inflater, parent);
    }

    class MerchantViewHolder extends BaseListAdapter<MerchantSummary>.BaseViewHolder {

        private TextView mMerchantNameView;
        private TextView mMerchantSpendingView;
        private TextView mMerchantDistanceView;

        MerchantViewHolder(LayoutInflater inflater, ViewGroup parent) {
            super(inflater.inflate(R.layout.list_item_merchant_summary, parent, false));
            mMerchantNameView = itemView.findViewById(R.id.merchant_name);
            mMerchantSpendingView = itemView.findViewById(R.id.merchant_average_spending);
            mMerchantDistanceView = itemView.findViewById(R.id.merchant_distance);
        }

        @Override
        public void bind(MerchantSummary summary) {
            mMerchantNameView.setText(summary.getMerchantName());
            mMerchantSpendingView.setText(summary.getMerchantAverageSpendingString());
            mMerchantDistanceView.setText(summary.getDistanceString());
        }
    }

}