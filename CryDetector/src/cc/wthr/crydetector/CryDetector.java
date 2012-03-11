package cc.wthr.crydetector;

import java.util.LinkedList;
import java.util.Queue;

import android.media.audiofx.Visualizer;
import android.media.audiofx.Visualizer.OnDataCaptureListener;
import android.util.Log;

public class CryDetector implements OnDataCaptureListener {
	private static final int SAMPLES_SIZE = 128;
	private static final double[] THETA = {
		  -8.1517e-01, -1.5732e-02,  1.5367e-02,  3.3554e-03, -6.8559e-02,
		   4.3358e-03, -3.6881e-02, -1.8017e-02, -2.2001e-02, -1.0980e-02,
		   3.0982e-02, -1.0952e-02,  5.1102e-02,  2.1196e-02, -4.3342e-03,
		   4.9652e-04, -5.6079e-03,  1.1776e-02,  1.5950e-02,  8.8128e-03,
		  -2.1805e-02,  1.1936e-02, -1.4101e-03,  1.6461e-02, -2.5867e-02,
		   2.0424e-02,  2.1441e-03,  1.2562e-02, -5.2674e-03, -2.0408e-02,
		  -2.7900e-02,  1.5443e-02, -3.6115e-02,  9.3116e-03,  4.0459e-03,
		  -4.2238e-02,  2.3775e-02, -3.5206e-02,  7.6117e-03, -3.3144e-02,
		   2.2565e-02,  8.1240e-04,  1.3841e-03,  6.1578e-03, -2.3703e-02,
		  -2.5899e-02,  1.3327e-03,  1.6749e-02,  2.7949e-02, -1.0154e-02,
		  -1.7290e-02, -1.2804e-02,  2.1805e-02,  3.2403e-02, -7.3487e-04,
		   3.7955e-02, -2.1565e-03,  2.4405e-02,  5.3632e-03, -1.9678e-02,
		   1.1958e-02, -3.0015e-03, -5.9488e-02,  5.6146e-03,  5.7743e-03,
		   9.8810e-03,  1.4486e-02,  3.0417e-02, -7.6167e-03,  3.0008e-02,
		   8.5387e-03, -2.6499e-02,  8.6976e-03, -1.4155e-03, -4.1249e-02,
		   2.5185e-02,  2.9742e-02,  5.7521e-03,  1.0888e-02, -2.9344e-02,
		  -6.1201e-02,  5.3292e-03,  5.4213e-03, -1.7443e-02, -2.1334e-02,
		  -3.2610e-02, -3.1148e-02, -3.1729e-02,  3.6813e-03,  3.5434e-02,
		  -1.5815e-02,  1.3062e-02,  3.3126e-02,  7.1708e-03, -3.4734e-02,
		  -3.2795e-02, -2.9517e-02,  1.8561e-02, -2.4819e-02, -3.6893e-02,
		  -2.8719e-02, -5.0618e-02,  3.6020e-02, -2.4774e-02, -4.8556e-02,
		   3.4297e-03,  2.8601e-02,  1.1389e-03,  8.6726e-03,  1.3724e-02,
		   6.7201e-02,  2.3277e-02,  5.5164e-02,  2.0055e-02, -3.0088e-02,
		   7.1869e-02, -2.4639e-02,  5.0893e-02,  3.7092e-02,  3.8686e-03,
		  -1.0652e-03,  2.0664e-02,  1.4788e-02, -1.1442e-03,  1.3960e-02,
		   2.5452e-02,  6.4401e-02,  5.9454e-02,  5.2253e-02
	};
	
	private byte mBytes[];
	private Visualizer mVisualizer = null;
	private ICryListener mCryListener = null;
	private Queue<Boolean> mCryFilter = new LinkedList<Boolean>();
	private int mCryFilterCount = 0;
	
	public CryDetector() {
		mBytes = new byte[SAMPLES_SIZE];
	}
	
	public void setCryListener(ICryListener cryListener) {
		mCryListener = cryListener;
	}
	
	public void link(int sessionId) {
		unlink();
		mVisualizer = new Visualizer(sessionId);
		mVisualizer.setCaptureSize(Visualizer.getCaptureSizeRange()[1]);
		mVisualizer.setDataCaptureListener(this, Visualizer.getMaxCaptureRate(), false, true);
		mVisualizer.setEnabled(true);
	}
	
	public void unlink() {
		if(mVisualizer != null) {			
			mVisualizer.setEnabled(false);
			//mVisualizer.release();
			mVisualizer = null;
			mCryFilter.clear();
			mCryFilterCount = 0;
		}
	}

	public void onFftDataCapture(Visualizer visualizer, byte[] fft,
			int samplingRate) {
		for (int i = 0; i < SAMPLES_SIZE; i++) {
			byte rfk = fft[2 * i];
			byte ifk = fft[2 * i + 1];
			float magnitude = (rfk * rfk + ifk * ifk);
			if(magnitude == 0) {
				mBytes[i] = 0;
			} else {
				mBytes[i] = (byte) (10*Math.log10(magnitude));
			}
		}
		
		/*
		StringBuilder builder = new StringBuilder("[");
		for (int i = 0; i < mBytes.length; i++) {
			builder.append(mBytes[i]);
            if(i != mBytes.length-1) {
		        builder.append(", ");
            }
		}		
		Log.d("CRY_0", builder.toString());
		*/
		classityBytes();
	}

	private void classityBytes() {
		double result = THETA[0];
		for(int i=0; i<SAMPLES_SIZE; i++) {
			result += mBytes[i] * THETA[i+1];
		}
		boolean isCry = 1/(1 + Math.exp(-1 * result)) > 0.5;
		if(mCryListener != null) {
			mCryListener.onSampleReceived();
		}
		addSample(isCry);
	}

	private void addSample(Boolean sample) {
		if(sample) {
			mCryFilterCount ++;
		}
		
		mCryFilter.offer(sample);
		if(mCryFilter.size() > 7) {
			Boolean prev = mCryFilter.poll();
			if(prev) {
				mCryFilterCount--;
			}
		}
		if(mCryFilterCount>=5 && sample) {
			if(mCryListener != null) {
				mCryListener.onCryReceived();
				mCryFilter.clear();
				mCryFilterCount = 0;
			}
		}
		
	}
	
	public void onWaveFormDataCapture(Visualizer visualizer, byte[] waveform,
			int samplingRate) {
		/* Not used */
	}
	
	public interface ICryListener {
		public void onCryReceived(); 
		public void onSampleReceived();
	}
}
