from bs4 import BeautifulSoup
import requests
import pandas as pd

#获取URL
def get_page_content(request_url):
	headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)\
		 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
	html=requests.get(request_url,headers=headers,timeout=10)
	content = html.text
	soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
	return soup


#页面分析函数
def analysis(soup):
	table = soup.find('div',class_="tslb_b")
	#找出所有行
	tr_list=table.find_all('tr')
	df=pd.DataFrame(columns=['id','brand','car_model','car_type','desc','problem','datetime','status'])
	for tr in tr_list:
		td_list=tr.find_all('td')
		if len(td_list)>0:
			id,brand,car_model,car_type,desc,problem,datetime,status=\
				td_list[0].text,td_list[1].text,td_list[2].text,td_list[3].text,\
				td_list[4].text,td_list[5].text,td_list[6].text,td_list[7].text
			temp={}
			temp['id']=id
			temp['brand']=brand
			temp['car_model']=car_model
			temp['car_type']=car_type
			temp['desc']=desc
			temp['problem']=problem
			temp['datetime']=datetime
			temp['status']=status
			df=df.append(temp,ignore_index=True)
	return df

#翻页函数
def get_several_page(base_url):
	result=pd.DataFrame(columns=['id','brand','car_model','car_type','desc','problem','datetime','status'])
	for i in range(20):
		url=base_url+str(i+1)+'.shtml'
		soup=get_page_content(url)
		result=result.append(analysis(soup),ignore_index=True)
	return result

base_url='http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-'
result=get_several_page(base_url)
print(result)
result.to_csv('car_complain.csv',index=False)
result.to_excel('car_complain.xlsx',index=False)
