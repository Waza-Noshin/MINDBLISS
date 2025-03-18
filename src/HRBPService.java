package com.mindbliss;

import android.util.Log;
import com.samsung.android.sdk.accessory.SAAgentV2;
import com.samsung.android.sdk.accessory.SASocket;

public class HRBPService extends SAAgentV2 {

    private static final String TAG = "HRBPService";

    public HRBPService() {
        super(TAG, HRBPChannel.class);
    }

    private class HRBPChannel extends SASocket {
        protected HRBPChannel() {
            super(HRBPChannel.class.getName());
        }

        @Override
        public void onReceive(int channelId, byte[] data) {
            String receivedData = new String(data);
            Log.d(TAG, "Received HR/BP: " + receivedData);
        }

        @Override
        public void onError(int channelId, String errorMessage, int errorCode) {
            Log.e(TAG, "Error in channel: " + errorMessage + " Code: " + errorCode);
        }

        @Override
        public void onServiceConnectionLost(int errorCode) {
            Log.w(TAG, "Service connection lost: " + errorCode);
        }
    }
}
