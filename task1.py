import pandas as pd
import matplotlib.pyplot as plt

def exercise_0(file):
    dataframe = pd.read_csv(file)
    return dataframe

def exercise_1(df):
    column_names = list(df.columns)
    return column_names

def exercise_2(df, k):
    sample = df.head(k)
    return sample

def exercise_3(df, k):
    sample = df.sample(k)
    return sample

def exercise_4(df):
    unique = df.dtypes.unique()
    return unique

def exercise_5(df):
    transaction_counts = df.value_counts().head(10).reset_index(name='frequency')     
    return transaction_counts

def exercise_6(df):
    fraudulent = df[df['isFraud'] == 1]
    return fraudulent

def exercise_7(df):
    distinct = df.groupby('nameOrig')['nameDest'].nunique().reset_index(name='distinct_destinations')
    distinct = distinct.sort_values(by='distinct_destinations', ascending=False)
    return distinct

def visual_1(df):
    def transaction_counts(ax):
        df['type'].value_counts().plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title('Frequency of Transaction Types')
        ax.set_xlabel('Transaction Type')
        ax.set_ylabel('Count')
        ax.tick_params(axis='x', rotation=45)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2, p.get_height()), 
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    def transaction_counts_split_by_fraud(ax):
        df.groupby(['type', 'isFraud']).size().unstack().plot(kind='bar', stacked=True, color=['lightcoral', 'lightgreen'], ax=ax)
        ax.set_title('Transaction Types Split by Fraud')
        ax.set_xlabel('Transaction Type')
        ax.set_ylabel('Count')
        ax.tick_params(axis='x', rotation=45)
        ax.legend(title='Fraud', labels=['Not Fraud', 'Fraud'])
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2, p.get_height()), 
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    fig, axs = plt.subplots(2, figsize=(12, 10))
    transaction_counts(axs[0])
    transaction_counts_split_by_fraud(axs[1])
    
    fig.suptitle('Transaction Type Analysis')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

def visual_2(df):
    def query(df):
        # Filtrar para transações 'CASH_OUT'
        cash_out_df = df[df['type'] == 'CASH_OUT'].copy()
        # Calcular as diferenças de saldo
        cash_out_df['deltaOrig'] = cash_out_df['oldbalanceOrg'] - cash_out_df['newbalanceOrig']
        cash_out_df['deltaDest'] = cash_out_df['newbalanceDest'] - cash_out_df['oldbalanceDest']
        return cash_out_df[['deltaOrig', 'deltaDest']]
    
    # Gerar o DataFrame filtrado e calculado
    plot_data = query(df)
    
    # Plotar o gráfico de dispersão
    plt.figure(figsize=(10, 6))
    plot_data.plot.scatter(x='deltaOrig', y='deltaDest', alpha=0.6, color='blue')
    plt.title('Origin vs. Destination Account Balance Delta for Cash Out Transactions')
    plt.xlabel('Origin Account Balance Delta')
    plt.ylabel('Destination Account Balance Delta')
    plt.xlim(left=-1e3, right=1e3)
    plt.ylim(bottom=-1e3, top=1e3)
    plt.tight_layout()
    plt.show()

def exercise_custom(df):
    grouped = df.groupby(['type', 'isFraud'])['amount'].agg(['mean', 'median']).unstack()
    return grouped
    
def visual_custom(df):
    grouped = exercise_custom(df)

    fig, axs = plt.subplots(2, figsize=(12, 12))

    grouped['mean'].plot(kind='bar', ax=axs[0], color=['skyblue', 'salmon'])
    axs[0].set_title('Mean Transaction Amount by Type and Fraud Status')
    axs[0].set_xlabel('Transaction Type')
    axs[0].set_ylabel('Mean Amount')
    axs[0].legend(['Not Fraud', 'Fraud'])
    axs[0].tick_params(axis='x', rotation=45)

    grouped['median'].plot(kind='bar', ax=axs[1], color=['skyblue', 'salmon'])
    axs[1].set_title('Median Transaction Amount by Type and Fraud Status')
    axs[1].set_xlabel('Transaction Type')
    axs[1].set_ylabel('Median Amount')
    axs[1].legend(['Not Fraud', 'Fraud'])
    axs[1].tick_params(axis='x', rotation=45)

    fig.suptitle('Transaction Amount Analysis by Type and Fraud Status')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
