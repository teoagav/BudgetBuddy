package com.example.budgetbuddy.interfaces;


import androidx.fragment.app.Fragment;

public interface FragmentInteractionListener {

    /**
     * Replaces the current fragment with childFragment
     *
     * @param childFragment replaces current fragment with this
     * @param tag           tag for fragment transaction
     */
    void startFragment(Fragment childFragment, String tag);

    /**
     * Sets the title of the app bar
     *
     * @param title string res of the fragment's title
     */
    void setTitle(String title);
}
