package com.net;

import java.awt.BorderLayout;
import java.awt.FlowLayout;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class TraceRoute {
	private JFrame jf;
	private JButton jb;
	private JTextField jtf;
	private ButtonListener btl;
	private JTextArea jta;
	private JPanel jp;
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		TraceRoute tr = new TraceRoute();
	}
	
	public TraceRoute (){
		UI();
		
	}
	
	public void UI(){
		jf = new JFrame();
		jf.setTitle("计网UI界面");
		jf.setLocation(450, 100);
		jf.setSize(550, 600);
		jf.setLayout(new BorderLayout());
		jp = new JPanel();
		jta = new JTextArea();
		jta.setEditable(false);
		jtf = new JTextField(40);
		jp.add(jtf);
		jb = new JButton("启动");
		btl = new ButtonListener(jtf, jta);
		jb.addActionListener(btl);
		jp.add(jb);
		jf.add(jta, "Center");
		jf.add(jp, "North");
		jf.setResizable(false);
		jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		jf.setVisible(true);
	}
}
