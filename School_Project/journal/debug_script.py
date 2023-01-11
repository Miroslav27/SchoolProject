if __name__=="__main__":
    from journal.models import Currency
    from journal.parsers import parse_all

    results = parse_all()
    for result in results:
        if result:
            instance = Currency.objects.create(
                broker=result["broker"], usd_buy=result["usd_buy"], usd_sell=result["usd_sell"],
                eur_buy=result["eur_buy"], eur_sell=result["eur_sell"],
                            )
            print(instance)
            #instance.save()