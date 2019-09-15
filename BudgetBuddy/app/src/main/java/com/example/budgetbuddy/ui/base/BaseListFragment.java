package com.example.budgetbuddy.ui.base;

import android.os.Bundle;
import android.os.Parcelable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.budgetbuddy.R;
import com.example.budgetbuddy.adapters.BaseListAdapter;
import com.example.budgetbuddy.listeners.RecyclerItemClickListener;

import java.util.ArrayList;
import java.util.List;

/**
 * Base class for general list fragment.
 *
 * @param <K> {@inheritDoc}
 * @param <D> List of this type
 */
public abstract class BaseListFragment
        <K extends Parcelable, D extends Parcelable>
        extends BaseDataFragment<K, List<D>> {

    private RecyclerView mRecyclerView;
    private BaseListAdapter mAdapter;
    private TextView mTopText;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_base_list, container, false);
    }

    @Override
    public void updateUI() {
        setTitle(getTitle());
        boolean showViews = getData() != null && getData().size() != 0;
        if (showViews) {
            mTopText.setText(getListDescription());
            if (mAdapter == null || mRecyclerView.getAdapter() != mAdapter) {
                mAdapter = createAdapter(getData());
                mRecyclerView.setAdapter(mAdapter);
            } else {
                mAdapter.setData(getData());
                mAdapter.notifyDataSetChanged();
            }
        }
        setViewsVisibility(showViews);
    }

    @Override
    public void initialiseViews(View view) {
        mRecyclerView = view.findViewById(R.id.recycler_view);
        mRecyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));
        DividerItemDecoration dividerItemDecoration = new DividerItemDecoration(mRecyclerView.getContext(),
                ((LinearLayoutManager) mRecyclerView.getLayoutManager()).getOrientation());
        mRecyclerView.addItemDecoration(dividerItemDecoration);
        mAdapter = createAdapter(new ArrayList<D>());
        mRecyclerView.setAdapter(mAdapter);
        mRecyclerView.addOnItemTouchListener(
                new RecyclerItemClickListener(getContext(), mRecyclerView, new RecyclerItemClickListener.OnItemClickListener() {
                    @Override
                    public void onItemClick(View view, int position) {
                        onListItemClick(position);
                    }

                    @Override
                    public void onLongItemClick(View view, int position) {
                    }
                })
        );
        mTopText = view.findViewById(R.id.list_description);
    }

    private void setViewsVisibility(boolean showViews) {
        mRecyclerView.setVisibility(showViews ? View.VISIBLE : View.GONE);
        mTopText.setVisibility(showViews ? View.VISIBLE : View.GONE);
        getView().findViewById(R.id.empty_text).setVisibility(showViews ? View.GONE : View.VISIBLE);
    }

    public abstract BaseListAdapter createAdapter(List<D> data);

    public abstract void onListItemClick(int position);

    public abstract String getListDescription();

    public abstract String getTitle();
}


