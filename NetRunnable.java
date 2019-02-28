package com.net;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import javax.swing.JTextArea;
import javax.swing.JTextField;

public class NetRunnable implements Runnable{
	private JTextField jtf;
	private JTextArea jta;
	private Process p;
	private String tracert = "tracert -h 100 ";
//	private String url = "http://www.ip138.com/";
	private String ping = "ping -n 100 ";
	private String s;
	public NetRunnable(JTextArea jta, JTextField jtf, String s){
		this.jta = jta;
		this.jtf = jtf;
		if(s.equals("追踪")){
			this.s = this.tracert;
		} else if(s.equals("ping")){
			this.s = this.ping;
		}
	}
	@Override
	public void run() {
		// TODO Auto-generated method stub
		String text = jtf.getText();
		String cmd = s + text;
		String str = null;
		Process p = null;
		boolean tmp = false;
		int time = 0;
		int data = 0;
		double datawidth = 0;
		try {
			p = Runtime.getRuntime().exec(cmd);
			BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
			
			if(cmd.contains("ping")){
				while((str = br.readLine()) != null){
					if(str.contains("平均")){
						String str1 = str.substring(str.indexOf("平均"), str.length());
						String str2 = str1.substring(str1.indexOf("平均")+5, str1.indexOf("ms"));
						time = Integer.parseInt(str2);
//						System.out.println(str2);
					}
					if(!tmp && str.contains("字节=")){
						tmp = true;
						String str1 = str.substring(str.indexOf("字节=")+3, str.indexOf(" 时间"));
						data = Integer.parseInt(str1);
					}
//					System.out.println("时间是："+time+"\n");
//					System.out.println("数据大小是： "+data+"\n");
					jta.append(str+"\n");
					System.out.println(str);
				}
				datawidth = ((data*16000)/time);
				jta.append("带宽为: "+datawidth+" bps\n");
			} else {
				while((str = br.readLine()) != null){
					jta.append(str+"\n");
					System.out.println(str);
				}
			}
			br.close();
			p.destroy();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}	
	}
}
