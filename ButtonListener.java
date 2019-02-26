package com.net;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import javax.swing.JTextArea;
import javax.swing.JTextField;

public class ButtonListener implements ActionListener{
	private JTextField jtf;
	private JTextArea jta;
	private Process p;
	private String tracert = "tracert -h 100";
	public ButtonListener(JTextField jtf, JTextArea jta){
		this.jtf = jtf;
		this.jta = jta;
	}
	
	public void actionPerformed(ActionEvent e) {
		// TODO Auto-generated method stub
		jta.append(jtf.getText());
		fun();
//		jtf.setText("");
//		jta.setText("");
//		System.out.println("click");
//		jta.setText("click");
	}
	
	public void fun(){
		String text = jtf.getText();
		String cmd = this.tracert + " " + text;
		String str = null;
		try {
			p = Runtime.getRuntime().exec(cmd);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
		try {
			while(br.readLine() != null){
				str = br.readLine();
					jta.append(str+"\n");
					System.out.println(str);	
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		p.destroy();
		
	}
}
