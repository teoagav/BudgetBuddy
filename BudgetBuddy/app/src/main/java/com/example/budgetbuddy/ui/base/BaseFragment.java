package com.example.budgetbuddy.ui.base;

import android.content.Context;
import android.os.Bundle;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.example.budgetbuddy.interfaces.FragmentInteractionListener;

public class BaseFragment extends Fragment {

    private FragmentInteractionListener mListener;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setHasOptionsMenu(true);
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        if (getActivity() instanceof FragmentInteractionListener) {
            mListener = (FragmentInteractionListener) getActivity();
        } else {
            throw new RuntimeException("Host activity must implement FragmentInteractionListener");
        }
    }

    public void startFragment(Fragment fragment, String tag) {
        mListener.startFragment(fragment, tag);
    }

    public void setTitle(String title) {
        mListener.setTitle(title);
    }

}
