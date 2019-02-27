package com.net;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class TraceRoute implements  ActionListener{
	private JFrame jf;
	private JButton jb1;
	private JButton jb2;
	private JTextField jtf;
	private JTextArea jta;
	private JPanel jp;
	private JScrollPane jsp;
	private ArrayList<Thread> thArr = new ArrayList<Thread>();
	private int len = 0;
	private NetRunnable nr;
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		TraceRoute tr = new TraceRoute();
	}
	
	public TraceRoute (){
		UI();
	}
	public void UI(){
		jf = new JFrame();
		jf.setTitle("¼ÆÍøUI½çÃæ");
		jf.setLocation(450, 100);
		jf.setSize(550, 600);
		jf.setLayout(new BorderLayout());
		jp = new JPanel();
		jta = new JTextArea();
		jta.setEditable(false);
		jtf = new JTextField(30);
		jp.add(jtf);
		jb1 = new JButton("×·×Ù");
		jb2 = new JButton("ping");
		jb1.addActionListener(this);
		jb2.addActionListener(this);
		jp.add(jb1);
		jp.add(jb2);
		jsp = new JScrollPane(jta);
		jf.add(jsp, "Center");
		jf.add(jp, "North");
		jf.setResizable(false);
		jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		jf.setVisible(true);
		
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		nr = new NetRunnable(jta, jtf, e.getActionCommand());
		Thread r = new Thread(nr);
		thArr.add(r);
		r.start();
		
	}
}
