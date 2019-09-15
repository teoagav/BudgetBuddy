package com.example.budgetbuddy.ui.base;

import android.os.Bundle;
import android.os.Parcelable;
import android.view.View;
import android.widget.ProgressBar;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.loader.app.LoaderManager;
import androidx.loader.content.Loader;

import com.example.budgetbuddy.R;
import com.example.budgetbuddy.utils.ViewUtils;

/**
 * Base fragment for all fragments that display data
 *
 * @param <K> typeof key for identifying this and for retrieving data (eg. String for course code)
 * @param <D> typeof value this fragment will display (eg. List of CourseSummary)
 */
public abstract class BaseDataFragment<K extends Parcelable, D> extends BaseFragment {

    private static final int DATA_LOADER_ID = -9138;
    private static final String KEY_ARG = "key_arg";

    private K mKey;
    private D mData;
    private ProgressBar mProgressSpinner;

    public static <K extends Parcelable, F extends BaseDataFragment> F createFragment(F fragment, K key) {
        Bundle args = new Bundle();
        args.putParcelable(KEY_ARG, key);
        fragment.setArguments(args);
        return fragment;
    }

    /**
     * 1. get key from arguments, if it exists
     * 2. initialise views, which gets references to each view
     * 3. updateData(), which will eventually call updateUI()
     */
    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        if (getArguments() != null) {
            mKey = getArguments().getParcelable(KEY_ARG);
        }
        initialiseViews(view);
        mProgressSpinner = view.findViewById(R.id.progress_spinner);
        updateData();
    }

    public void setKey(K key) {
        mKey = key;
    }

    public K getKey() {
        return mKey;
    }

    public void setData(D data) {
        mData = data;
    }

    public D getData() {
        return mData;
    }

    /**
     * Re-fetches data associated with the current course summary
     */
    public void updateData() {
        getLoaderManager().restartLoader(DATA_LOADER_ID, null, new DataLoaderCallbacks());
    }

    /**
     * Called once the data in updateData() has been fetched - somewhere in the method chain of
     * a call to updateData(). Default behaviour is to call in Loader.OnLoadFinished
     */
    public abstract void updateUI();

    /**
     * Get access to all views via rootView.findViewById
     */
    public abstract void initialiseViews(View view);

    /**
     * @return data loader that loads the fragment's data from database
     */
    public abstract Loader<D> getDataLoader();

    /**
     * (Re)Loads data and then calls updateUI();
     */
    private class DataLoaderCallbacks implements LoaderManager.LoaderCallbacks<D> {
        @NonNull
        @Override
        public Loader<D> onCreateLoader(int id, Bundle args) {
            ViewUtils.setViewsVisibility(getView(), false);
            setContentVisibility(false);
            return getDataLoader();
        }

        @Override
        public void onLoadFinished(@NonNull Loader<D> loader, D data) {
            mData = data;
            boolean loadSuccessful = data != null;
            ViewUtils.setViewsVisibility(getView(), loadSuccessful);
            setContentVisibility(loadSuccessful);
            updateUI();
        }

        @Override
        public void onLoaderReset(@NonNull Loader<D> loader) {

        }
    }

    /**
     * @param show true if contents of this view should be shown, false if contents
     *             should be hidden and progress spinner should be shown
     */
    private void setContentVisibility(boolean show) {
        ViewUtils.setViewsVisibility(getView(), show);
        if (mProgressSpinner != null) {
            mProgressSpinner.setVisibility(show ? View.GONE : View.VISIBLE);
            mProgressSpinner.setEnabled(!show);
        }
    }
}
