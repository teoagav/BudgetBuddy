package com.example.budgetbuddy.ui;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.loader.content.Loader;

import com.example.budgetbuddy.R;
import com.example.budgetbuddy.loaders.MerchantDetailLoader;
import com.example.budgetbuddy.model.Merchant;
import com.example.budgetbuddy.model.MerchantSummary;
import com.example.budgetbuddy.ui.base.BaseDataFragment;

public class MerchantDetailFragment extends BaseDataFragment<MerchantSummary, Merchant> {

    private TextView mNameView;
    private TextView mAddressView;
    private TextView mDistanceView;
    private TextView mAverageSpendingView;
    private TextView mMedianSpendingView;
    private TextView mTransactionCountView;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_merchant_detail, container, false);
    }

    @Override
    public void updateUI() {
        if (getData() == null) {
            return;
        }
        mNameView.setText(getData().getName());
        mAddressView.setText(getData().getAddress() + ", " + getData().getCity());
        mDistanceView.setText(getData().getDistance());
        mAverageSpendingView.setText(getData().getAverageSpending());
        mMedianSpendingView.setText(getData().getMedianSpending());
        mTransactionCountView.setText(getData().getTransactionCount() + " transactions in the last 3 months");
    }

    @Override
    public void initialiseViews(View view) {
        mNameView = view.findViewById(R.id.merchant_name);
        mAddressView = view.findViewById(R.id.merchant_address);
        mDistanceView = view.findViewById(R.id.merchant_distance);
        mAverageSpendingView = view.findViewById(R.id.average_spending);
        mMedianSpendingView = view.findViewById(R.id.median_spending);
        mTransactionCountView = view.findViewById(R.id.transaction_count);
    }

    @Override
    public Loader getDataLoader() {
        return new MerchantDetailLoader(getContext(), getKey().getMerchantName(), getKey().getLatitude(), getKey().getLongitude());
    }
}
