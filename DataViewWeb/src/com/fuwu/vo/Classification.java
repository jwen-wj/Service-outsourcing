package com.fuwu.vo;

public class Classification {

//	private int id;
	private String context;
	private String type;
//	public Classification(int id, String context, String type) {
//		this.id = id;
//		this.context = context;
//		this.type = type;
//	}
	public Classification(String context, String type) {
		this.context = context;
		this.type = type;
	}
	public Classification(String context){
		this.context=context;
	}
//	public int getId() {
//		return id;
//	}
//	public void setId(int id) {
//		this.id = id;
//	}
	public String getContext() {
		return context;
	}
	public void setContext(String context) {
		this.context = context;
	}
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	@Override
	public String toString() {
		return "Classification [context=" + context + ", type=" + type + "]";
	}
	
	
}
