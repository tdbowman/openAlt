import flask

def authorDashboardLogic(mysql, mysql2):

    author_article_list = []
    author_doi_list = []
    #global mysql
    cursor = mysql.connection.cursor()

    #global mysql2
    # connect to crossrefeventdatamain
    cursor2 = mysql2.connection.cursor()

    # fetch the query parameter author_id from searchResults page
    author_id = str(flask.request.args.get("author_id"))

    author_sql = "SELECT name FROM dr_bowman_doi_data_tables.author where id ="+author_id+";"
    cursor.execute(author_sql)
    author_name = cursor.fetchone()

    author_sql = "SELECT fk FROM dr_bowman_doi_data_tables.author where name = '" + \
        author_name['name'] + "';"
    cursor.execute(author_sql)
    author_resultset = cursor.fetchall()
    # form a list of fk for the where statement (ex.) ('2005','2006')
    author_fk_list = '('
    for row in author_resultset:
        # author_name=row['name']
        if row == author_resultset[-1]:
            author_fk_list = author_fk_list + str(row['fk'])
        else:
            author_fk_list = author_fk_list + str(row['fk']) + ","
    author_fk_list = author_fk_list + ')'

    #author_name = author_resultset['name']
    #author_fk = author_resultset['fk']
    if author_fk_list is not None:
        # look up author table by fk
        sql = "Select doi, title, container_title, published_print_date_parts, fk from _main_ where fk in " + \
            author_fk_list + ";"
        cursor.execute(sql)
        result_set = cursor.fetchall()

        # iterate the result set
        for row in result_set:
            # get fk from _main_ table
            fk = row['fk']
            author_list = []
            if fk is not None:
                # look up author table by fk
                author_sql = "select id, name from author where fk = " + \
                    str(fk) + ";"
                cursor.execute(author_sql)
                # get list of authors for given fk
                author_list = cursor.fetchall()

            # create dict with _main_ table row and author list
            article = {'objectID': row['doi'], 'articleTitle': row['title'],
                       'journalName': row['container_title'],
                       'articleDate': row['published_print_date_parts'],
                       'author_list': author_list}
            author_article_list.append(article)
            author_doi_list.append(row['doi'])
        cursor.close()


    # Size of each list depends on how many years(in chartScript.js) you'd like to display.
    # Queries will be inserted within the array
    years_list = [2016, 2017, 2018, 2019, 2020]

    # form a list of just the DOIs
    doi_list = '( '
    for doi in author_doi_list:
        if doi == author_doi_list[-1]:
            doi_list = doi_list + "'" + str(doi) + "'"
        else:
            doi_list = doi_list + "'" + str(doi) + "'" + ","
    doi_list = doi_list + ')'

    # cambia event
    cambiaEvent = []
    for year in years_list:
        cambia_sql = "select count(objectID) count from crossrefeventdatamain.cambiaevent " \
                     "where substr(objectID,17) in " + doi_list + " " \
                     "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(cambia_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        cambiaEvent.append(event_count['count'])
    # cambiaEvent = [30, 20, 50, 10, 90]  # TBD - delete this line after we upload data in cambia event table for all these years

    # crossrefevent
    crossrefevent = []
    for year in years_list:
        crossref_sql = "select count(objectID) count from crossrefeventdatamain.crossrefevent " \
                       "where substr(objectID,17) in " + doi_list + " " \
                       "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(crossref_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        crossrefevent.append(event_count['count'])
    # crossrefevent = [5, 7, 14, 18, 25]; # TBD - delete this line after we upload data in cambia event table for all these years

    # dataciteevent
    dataciteevent = []
    for year in years_list:
        datacite_sql = "select count(objectID) count from crossrefeventdatamain.dataciteevent " \
                       "where substr(objectID,17) in " + doi_list + " " \
                       "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(datacite_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        dataciteevent.append(event_count['count'])
    # dataciteevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # f1000event
    f1000event = []
    for year in years_list:
        f1000_sql = "select count(objectID) count from crossrefeventdatamain.f1000event " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(f1000_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        f1000event.append(event_count['count'])


    # hypothesisevent
    hypothesisevent = []
    for year in years_list:
        hypothesis_sql = "select count(objectID) count from crossrefeventdatamain.hypothesisevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(hypothesis_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        hypothesisevent.append(event_count['count'])
    # hypothesisevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # newsfeedevent
    newsfeedevent = []
    for year in years_list:
        newsfeed_sql = "select count(objectID) count from crossrefeventdatamain.newsfeedevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(newsfeed_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        newsfeedevent.append(event_count['count'])
    # newsfeedevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # redditevent
    redditevent = []
    for year in years_list:
        reddit_sql = "select count(objectID) count from crossrefeventdatamain.redditevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(reddit_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        redditevent.append(event_count['count'])
    # redditevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # redditlinksevent
    redditlinksevent = []
    for year in years_list:
        redditlinks_sql = "select count(objectID) count from crossrefeventdatamain.redditlinksevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(redditlinks_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        redditlinksevent.append(event_count['count'])
    # redditlinksevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # stackexchangeevent
    stackexchangeevent = []
    for year in years_list:
        stackexchange_sql = "select count(objectID) count from crossrefeventdatamain.stackexchangeevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(stackexchange_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        stackexchangeevent.append(event_count['count'])
    # stackexchangeevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # twitterevent
    twitterevent = []
    for year in years_list:
        twitter_sql = "select count(objectID) count from crossrefeventdatamain.twitterevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(twitter_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        twitterevent.append(event_count['count'])
    # twitterevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # webevent
    webevent = []
    for year in years_list:
        web_sql = "select count(objectID) count from crossrefeventdatamain.webevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(web_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        webevent.append(event_count['count'])
    # webevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # wikipediaevent
    wikipediaevent = []
    for year in years_list:
        wikipedia_sql = "select count(objectID) count from crossrefeventdatamain.wikipediaevent " \
            "where substr(objectID,17) in " + doi_list + " " \
            "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wikipedia_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        wikipediaevent.append(event_count['count'])
    # wikipediaevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years

    # wordpressevent
    wordpressevent = []
    for year in years_list:
        wordpress_sql = "select count(objectID) count from crossrefeventdatamain.wordpressevent " \
                        "where substr(objectID,17) in " + doi_list + " " \
                        "and substr(occurredAt,1,4)='" + str(year) + "';"

        cursor2.execute(wordpress_sql)
        mysql2.connection.commit()
        event_count = cursor2.fetchone()
        wordpressevent.append(event_count['count'])
    # wordpressevent = [5, 10, 15, 20, 25];  # TBD - delete this line after we upload data in cambia event table for all these years
    
    cursor2.close()

    return flask.render_template('authorDashboard.html',
                                 author_name=author_name['name'],
                                 author_article_list=author_article_list,
                                 cambiaEventData=cambiaEvent,
                                 crossrefeventdatamain=crossrefevent,
                                 f1000eventData=f1000event,
                                 dataciteEventData=dataciteevent,
                                 hypothesisEventData=hypothesisevent,
                                 newsfeedEventData=newsfeedevent,
                                 redditEventData=redditevent,
                                 redditlinksEventData=redditlinksevent,
                                 stackexchangeEventData=stackexchangeevent,
                                 twitterEventData=twitterevent,
                                 webEventData=webevent,
                                 wikipediaEventData=wikipediaevent,
                                 wordpressEventData=wordpressevent)
