
# Command types

There are six broad types for all of the search commands: distributable streaming, centralized streaming, transforming, generating, orchestrating and dataset processing. These types are not mutually exclusive. A command might be streaming or transforming, and also generating.

The following tables list the commands that fit into each of these types. For detailed explanations about each of the types, see Types of commands in the Search Manual .

To find out how the types of commands used in searches can affect performance, see Write better searches in the Search Manual .


## Streaming commands

A streaming command operates on each event as the event is returned by a search.

- A distributable streaming command runs on the indexer or the search head, depending on where in the search the command is invoked. Any distributable streaming command that comes after a non-streaming command in the search is processed on the search head.

- A centralized streaming command applies a transformation to each event returned by a search. Unlike distributable streaming commands, a centralized streaming command only works on the search head.




| Command | Notes |
| --- | --- |
| addinfo | Distributable streaming |
| addtotals | Distributable streaming. Atransformingcommand when used to calculate column totals (not row totals). |
| arules | Some of the work is distributable streaming running on the indexer or the search head. The rest of the work is centralized streaming running on the search head. |
| autoregress | Centralized streaming. |
| bin | Streaming if specified with thespanargument. Otherwise a dataset processing command. |
| bucketdir | Distributable streaming by default, but centralized streaming if thelocalsetting specified for the command in the commands.conf file is set to true. |
| cluster | Streaming in some modes. |
| convert | Distributable streaming. |
| dedup | Distributable streaming in a prededup phase. Centralized streaming after the individual indexers perform their own dedup and the results are returned to the search head from each indexer.Using thesortbyargument or specifyingkeepevents=truemakes thededupcommand a dataset processing command. |
| eval | Distributable streaming. |
| extract | Distributable streaming. |
| fieldformat | Distributable streaming. |
| fields | Distributable streaming. |
| fillnull | Distributable streaming when afield-listis specified. Adataset processingcommand when nofield-listis specified. |
| head | Centralized streaming. |
| highlight | Distributable streaming. |
| iconify | Distributable streaming. |
| iplocation | Distributable streaming. |
| join | Centralized streaming, if there is a defined set of fields to join to. Adataset processingcommand when nofield-listis specified. |
| lookup | Distributable streaming when specified withlocal=false, which is the default. Anorchestratingcommand whenlocal=true. |
| makemv | Distributable streaming. |
| multikv | Distributable streaming. |
| mvexpand | Distributable streaming. |
| nomv | Distributable streaming. |
| rangemap | Distributable streaming. |
| regex | Distributable streaming. |
| reltime | Distributable streaming. |
| rename | Distributable streaming. |
| replace | Distributable streaming. |
| rex | Distributable streaming. |
| search | Distributable streaming if used further down the search pipeline. Ageneratingcommand when it is the first command in the search. |
| spath | Distributable streaming. |
| strcat | Distributable streaming. |
| streamstats | Centralized streaming. |
| tags | Distributable streaming. |
| transaction | Centralized streaming. |
| typer | Distributable streaming. |
| where | Distributable streaming. |
| untable | Distributable streaming. |
| xmlkv | Distributable streaming. |
| xmlunescape | Distributable streaming by default, but centralized streaming if thelocalsetting specified for the command in the commands.conf file is set to true. |
| xpath | Distributable streaming. |
| xyseries | Distributable streaming if the argumentgrouped=falseis specified, which is the default. Otherwise atransformingcommand. |



## Generating commands

A generating command either returns information or generates results. Some generating commands can return information from an index, a data model, a lookup, or a CSV file without any transformations to the information. Other generating commands generate results, usually for testing purposes.


| Command | Notes |
| --- | --- |
| datamodel | Report-generating |
| dbinspect | Report-generating. |
| eventcount | Report-generating. |
| from | Can be either report-generating or event-generating depending on the search or knowledge object that is referenced by the command. |
| gentimes | Event-generating. |
| history | Report-generating. |
| inputcsv | Event-generating (centralized). |
| Inputlookup | Event-generating (centralized) whenappend=false, which is the default. |
| loadjob | Event-generating (centralized). |
| makeresults | Report-generating. |
| metadata | Report-generating. Although metadata fetches data from all peers, any command run after it runs only on the search head. |
| metasearch | Event-generating. |
| mstats | Report-generating, except whenappend=trueis specified. |
| multisearch | Event-generating. |
| pivot | Report-generating. |
| rest |  |
| search | Event-generating (distributable) when the first command in the search, which is the default. Astreaming(distributable) command if used later in the search pipeline. |
| searchtxn | Event-generating. |
| set | Event-generating. |
| tstats | Report-generating (distributable), except whenprestats=true. Whenprestats=true, thetstatscommand is event-generating. |
| typeaheadNo Content found for http://docs.splunk.com/Documentation/Splunk/10.0.0/SearchReference/Typeahead | Event-generating. |
| walklexNo Content found for http://docs.splunk.com/Documentation/Splunk/10.0.0/SearchReference/Walklex | Event-generating. |



## Transforming commands

A transforming command orders the results into a data table. The command "transforms" the specified cell values for each event into numerical values for statistical purposes.


> **Note: In earlier versions of Splunk software, transforming commands were called reporting commands.**



| Command | Notes |
| --- | --- |
| addtotals | Transforming when used to calculate column totals (not row totals). A distributablestreamingcommand when used to calculate row totals, which is the default. |
| anomalydetection |  |
| append |  |
| associate |  |
| chart |  |
| cofilter |  |
| contingency |  |
| history |  |
| makecontinuous |  |
| mvcombine |  |
| rare |  |
| stats |  |
| table |  |
| timechart |  |
| top |  |
| xyseries | Transforming ifgrouped=true. Astreaming(distributable) command whengrouped=false, which is the default setting. |



## Orchestrating commands

Orchestrating commands control some aspect of how a search is processed. They do not directly affect the final result set of the search. For example, you might apply an orchestrating command to a search to enable or disable a search optimization that helps the overall search complete faster.


| Command | Notes |
| --- | --- |
| localop |  |
| lookup | Only becomes an orchestrating command whenlocal=true. This forces thelookupcommand to run on the search head and not on any remote peers. Astreaming(distributable) command whenlocal=false, which is the default setting. |
| noop |  |
| redistribute |  |
| require |  |



## Dataset processing commands

A dataset processing command is a command that requires the entire dataset before the command can run. Some of these commands fit into other command types in specific situations or when specific arguments are used.


| Command | Notes |
| --- | --- |
| anomalousvalue | Some modes |
| anomalydetection | Some modes |
| append | Some modes |
| appendcols |  |
| appendpipe |  |
| bin | Some modes. Astreamingcommand if thespanargument is specified. |
| cluster | Some modes |
| concurrency |  |
| datamodel |  |
| dedup | Using thesortbyargument or specifyingkeepevents=truemakes thededupcommand a dataset processing command. Otherwise,dedupis a distributable streaming command in a prededup phase. Centralized streaming after the individual indexers perform their own dedup and the results are returned to the search head from each indexer. |
| eventstats |  |
| fieldsummary |  |
| fillnull | When nofield-listis specified, a dataset processing command. If afield-listis specifiedfillnullis adistributable streamingcommand. |
| from | Some modes |
| join | Some modes. Acentralized streamingcommand when there is a defined set of fields to join to. |
| map |  |
| outlier |  |
| reverse |  |
| sort |  |
| tail |  |
| transaction | Some modes |
| union | Some modes |
