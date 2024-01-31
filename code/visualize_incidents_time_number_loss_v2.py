import pandas as pd
import matplotlib.pyplot as plt

# Process the raw data and save the processed data as a CSV file
def process_and_save_data():
    # Read the raw data
    df = pd.read_csv('./data/Bridge_Real_Life_Attack_Incidents_Info_1017.csv',encoding='utf-8')

    # Convert the date column to a date type
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')

    # Extract year and month information
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # Get the minimum year and month from the raw data
    min_year = df['Year'].min()
    min_month = df[df['Year'] == min_year]['Month'].min()

    # Get the maximum year and month from the raw data
    max_year = df['Year'].max()
    max_month = df[df['Year'] == max_year]['Month'].max()

    # Create a date range with all months
    date_range = pd.date_range(start=f'{int(min_year)}-{int(min_month):02d}-01', 
                              end=f'{int(max_year)}-{int(max_month):02d}-01', 
                              freq='MS')
    all_months = pd.DataFrame({'Year': date_range.year, 'Month': date_range.month})

    # Merge the raw data with the data containing all months
    df = pd.merge(all_months, df, on=['Year', 'Month'], how='left')

    # Fill missing values with 0
    df['Amount lost (in Million USD)'] = df['Amount lost (in Million USD)'].fillna(0)

    # Summarize data by year and month
    monthly_summary = df.groupby(['Year', 'Month']).agg({'Amount lost (in Million USD)': 'sum', 'Date': 'count'}).reset_index()
    monthly_summary.rename(columns={'Amount lost (in Million USD)': 'Total Loss (Million USD)', 'Date': 'Number of Incidents'}, inplace=True)

    # Save the processed data as a CSV file
    monthly_summary.to_csv('Data/Bridge_Attack_monthly_summary.csv', index=False)


#  Plot the chart
def plot_chart():
    # Read the processed CSV file
    df = pd.read_csv('Data/Bridge_Attack_monthly_summary.csv')

    # Create a figure and axis object
    fig, ax1 = plt.subplots(figsize=(10, 5))

    #Mapping for different Month format
    month_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    df['Month_Name'] = df['Month'].map(month_map)

    #Date used in Month-Year format
    df['Date'] =  df['Month_Name'].astype(str)+  '-' +  df['Year'].astype(str)

    # Plot a line chart representing the number of incidents
    ax1.plot(df['Date'], df['Number of Incidents'], color='black', label='Number of Incidents', marker='o', linestyle = "--",markerfacecolor = "none", alpha=0.7 )
    ax1.set_xlabel('Date', fontsize=14,fontweight='bold')
    # ax1.set_ylabel('Number of Incidents', color='black', fontsize=14)
    ax1.set_ylabel('Frequency', color='black', fontsize=14, fontweight='bold')
    ax1.tick_params('y', colors='black', labelsize=10)
    
    # Rotate x-axis labels 
    fig.autofmt_xdate(rotation=70)

    # Create a second y-axis for the total loss
    ax2 = ax1.twinx()

    # Plot a bar chart representing the total loss amount, and set the legend label as "Total Loss"
    ax2.bar(df['Date'], df['Total Loss (Million USD)'], color='red', alpha=0.4, label='Total Loss (Million USD)')
    ax2.tick_params('y', labelsize=10)
    ax1.set_ylim(0,7)
    ax2.set_ylim(0,700)
    ax1.set_xlim("Jun-2021", "Sep-2023")
   
    # Improve the readability of the plot
    ax1.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)

    # Add legends for the line chart and bar chart, placing them in the upper right corner, vertically stacked, with shorter legend item length
    ax1.legend(loc='upper left', fontsize=10)
    ax2.legend(loc='upper right', fontsize=10)


    # Add a title to the plot
    plt.title('Monthly Bridge Attack Incidents and Total Loss', fontsize=16,fontweight='bold')

    # Save the chart as a PDF file
    plt.savefig('./figures/Fig_Incident_time_num_loss.pdf', format='pdf', bbox_inches='tight')

    # Show the chart
    plt.show()

if __name__ == "__main__":
    process_and_save_data()
    plot_chart()

