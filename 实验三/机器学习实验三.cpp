#include<iostream>
#include<cmath>
#include<vector>
#include<ctime>
#include<fstream>
using namespace std;
typedef unsigned int uint;
int fortime = 0;
struct Cluster
{
	vector<double> centroid;
	vector<uint> samples;
};
//计算距离
double cal_distance(vector<double> a, vector<double> b)
{

	uint len = a.size();
	double val = 0.0;
	for (uint i = 0; i < len; ++i)
	{
		val += pow((a[i] - b[i]), 2);
	}
	return sqrt(val);
}
//核心算法函数
vector<Cluster> k_means(vector<vector<double>> trainX, uint k)
{
	const uint row_num = trainX.size();
	const uint col_num = trainX[0].size();
	/*初始化聚类中心*/
	vector<Cluster> clusters(k);
	uint seed = (uint)time(NULL);
	/*随机选择出k个聚类中心*/
	for (uint i = 0; i < k; i++)
	{
		srand(seed);
		int c = rand() % row_num;
		clusters[i].centroid = trainX[c];
		seed = rand();
	}
	vector<vector<double>> check(k, vector<double>(2, 0.0));
	uint flag = 0;
	/*检验是否收敛，若聚类中心不再变化则停止更新，结果收敛*/
	while (flag < 3)
	{
		fortime++;
		/*储存当前聚类中心，用于判断是否收敛*/
		for (uint i = 0; i < k; ++i) {
			check[i] = clusters[i].centroid;
		}
		/*每一次重新计算样本点所属类别之前，清空原来样本点信息*/
		for (uint i = 0; i < k; ++i)
		{
			clusters[i].samples.clear();
		}
		/*求出每个样本点应属于哪一个聚类*/
		for (uint j = 0; j < row_num; ++j)
		{
			/*先初始化为第0类，再做比较进行分类*/
			uint c = 0;
			double min_distance = cal_distance(trainX[j], clusters[c].centroid);
			for (uint i = 1; i < k; ++i)
			{
				double distance = cal_distance(trainX[j], clusters[i].centroid);
				if (distance < min_distance)
				{
					min_distance = distance;
					c = i;
				}
			}
			clusters[c].samples.push_back(j);
		}
		/*更新聚类中心*/
		for (uint i = 0; i < k; ++i)
		{
			vector<double> val(col_num, 0.0);
			for (uint j = 0; j < clusters[i].samples.size(); ++j)
			{
				uint sample = clusters[i].samples[j];
				for (uint d = 0; d < col_num; ++d)
				{
					val[d] += trainX[sample][d];
					if (j == clusters[i].samples.size() - 1)
						clusters[i].centroid[d] = val[d] / clusters[i].samples.size();
				}
			}
		}
		/*判断是否收敛*/
		int sign = 0;
		for (uint i = 0; i < k; ++i) {
			if (check[i] != clusters[i].centroid) {
				check[i] = clusters[i].centroid;
				sign++;
			}
		}
		if (sign == 0)
			flag++;
		else flag = 0;
	}
	return clusters;
}
int main()
{
	/*从txt文档独取样例数据*/
	fstream infile("E:\\test1.txt");
	double x, y;
	vector<vector<double>>ans;
	while (!infile.eof()) {
		infile >> x >> y;
		ans.push_back({ x,y });
	}
	infile.close();
	int len = ans.size();
	vector<vector<double>> trainX(len, vector<double>(2, 0.0));
	for (int i = 0; i < len; ++i) {
		trainX[i][0] = ans[i][0];
		trainX[i][1] = ans[i][1];
	}
	uint num;
	cout << "请输入聚类的中心数量：";
	cin >> num;
	/*k-means聚类*/
	vector<Cluster> clusters_out = k_means(trainX, num);
	/*输出分类结果*/
	for (uint i = 0; i < clusters_out.size(); i++)
	{
		cout << "第 " << i + 1 << " 个聚类中心:" << endl;
		/*子类中心*/
		cout << "\t" << "质心: " << "\n\t\t[ ";
		for (uint j = 0; j < clusters_out[i].centroid.size(); j++)
		{
			cout << clusters_out[i].centroid[j] << " ";
		}
		cout << "]" << endl;
		/*子类样本点*/
		cout << "\t" << "本组数据:\n";
		for (uint k = 0; k < clusters_out[i].samples.size(); k++)
		{
			uint c = clusters_out[i].samples[k];
			cout << "\t\t ";
			for (uint m = 0; m < trainX[0].size(); m++)
			{
				cout << trainX[c][m] << " ";
			}
			cout << "\n";
		}
	}
	
	system("pause");
	return 0;
}