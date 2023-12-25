from datetime import date, datetime


def json_encoder(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()


def generate_python_function_name(sentence: str):
    return sentence.lower().replace(" ", "_")


def count_monthly_visitor(timestamps: list[datetime]):
    counts_by_month = {}

    for timestamp in timestamps:
        year_month = timestamp.strftime("%Y-%m")
        counts_by_month[year_month] = counts_by_month.get(year_month, 0) + 1

    result = [{"month": key, "count": value} for key, value in counts_by_month.items()]
    result.sort(key=lambda x: x["month"])

    return result


def calculate_the_number_of_reads_per_article(articles):
    counts_by_article = {}

    for article in articles:
        counts_by_article[article] = counts_by_article.get(article, 0) + 1

    result = [
        {"article": key, "count": value} for key, value in counts_by_article.items()
    ]
    result.sort(key=lambda x: x["count"], reverse=True)
    return result


if __name__ == "__main__":
    sentence = "Make current user a global variable"
    print(generate_python_function_name(sentence))
