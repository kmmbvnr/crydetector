package cc.wthr.crydetector;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class MainActivity extends Activity implements OnClickListener {
    private Button mButtonCry1;
    private Button mButtonCry2;
    private Button mButtonCry3;
    private Button mButtonCry4;
    private Button mButtonNocry1;
    private Button mButtonNocry2;
    private Button mButtonNocry3;
    private Button mButtonNocry4;
    private Button mButtonMic;

	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        mButtonCry1 = (Button)findViewById(R.id.button_cry1);
        mButtonCry1.setOnClickListener(this);
        mButtonCry2 = (Button)findViewById(R.id.button_cry2);
        mButtonCry2.setOnClickListener(this);
        mButtonCry3 = (Button)findViewById(R.id.button_cry3);
        mButtonCry3.setOnClickListener(this);
        mButtonCry4 = (Button)findViewById(R.id.button_cry4);
        mButtonCry4.setOnClickListener(this);
        mButtonNocry1 = (Button)findViewById(R.id.button_nocry1);
        mButtonNocry1.setOnClickListener(this);
        mButtonNocry2 = (Button)findViewById(R.id.button_nocry2);
        mButtonNocry2.setOnClickListener(this);
        mButtonNocry3 = (Button)findViewById(R.id.button_nocry3);
        mButtonNocry3.setOnClickListener(this);
        mButtonNocry4 = (Button)findViewById(R.id.button_nocry4);
        mButtonNocry4.setOnClickListener(this);
        mButtonMic = (Button)findViewById(R.id.button_mic);
        mButtonMic.setOnClickListener(this);
    }

	public void onClick(View view) {
		if(view == mButtonCry1) {
			
		} else if(view == mButtonCry2) {
			
		} else if(view == mButtonCry3) {
			
		} else if(view == mButtonCry4) {
			
		} else if(view == mButtonNocry1) {
			
		} else if(view == mButtonNocry2) {
			
		} else if(view == mButtonNocry3) {
			
		} else if(view == mButtonNocry4) {
			
		}
	}
}