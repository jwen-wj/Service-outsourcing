package com.fuwu.dao;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;
import com.csvreader.CsvReader;
import com.fuwu.vo.Classification;

public class ReaderTest {
	static CsvReader csvReader ;
	static List<Classification> list_qList=new ArrayList<Classification>();
	public static void getReader(String filepath) throws FileNotFoundException {
		 //String filePath ="F:/apache-tomcat-9.0.6-windows-x64/apache-tomcat-9.0.6/webapps/fuwu/UpLoad_3.1/test.tsv";
		 String filePath=filepath;
		 csvReader=new CsvReader(filePath, ',', Charset.forName("utf-8"));
		//	new CsvReader(filePath);
		csvReader.setSafetySwitch(false); 
	}
	public static int sumrow(){
		int num=0;
		try {
			while (csvReader.readRecord()==true) {
				num++;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return num;
	}
	
	public static List<Classification> read(int num) throws FileNotFoundException{
		if(list_qList!=null){
			list_qList.clear();
		}
        try {
            int i=0;
            while (i<num+100){
            	if(csvReader.readRecord()!=false){
            		//csvReader.readRecord();
                	
                	System.out.println(csvReader.get(0));
                    // ¶ÁÒ»ÕûÐÐ
                	if(i>=num&&i!=0){
                		Classification classification=new Classification(csvReader.get(0));
//                		System.out.println(csvReader.get(0));
                		//System.out.println(classification.toString());
//                		System.out.println(list_qList);
                		list_qList.add(classification);
                	}
                    i++;
                    System.out.println(i);
            	}else {
					break;
				}
            	
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return list_qList;
    }
	public static void main(String[] args) throws FileNotFoundException {
		getReader("");
		read(1);
	}
}
