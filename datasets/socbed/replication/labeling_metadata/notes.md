### Notes regarding mapping of certain fields that had no clear counterpart in the logs
- `DestinationIsIPv6`
  - Field and value only occurs in the `message` field and nowhere else
- `Hashes`
  - Field itself only occurs in `message`, values (as in lists) can be found elsewhere
  - Question is, do we choose imphash, md5 or sha256?
- `Path`
  - Appears both in `registry.path` and `file.path`, while elastic.com lists it as `winlog.event_data.Path`
  - Only appears in Sigma rule "windows/builtin/windefend/win_defender_alert_lsass_access.yml" where it is checked for the value `\lsass.exe`, so I'm guessing `file.path`
- `QueryName`
  - Seems to be the same for `dns.question.name` and `winlog.event_data.QueryName`
- `QueryResults`
  - Field itself only occurs in `messsage`, value can partially be found elsewhere, i.e. the first part is missing
  - Sigma rules using that field are specifically checking for that first part
- `Signed`
  - Seems to be the same for `file.code_signature.signed` and `winlog.event_data.Signed`
- `Type`
  - Multiple occurrences with different meanings (`agent.type`, `winlog.user.type`, `network.type`, `event.type`, `dns.answers.type`, `registry.data.type`)
- `Value`
  - Contrary to the ambiguous name, this field exclusively occurs in `registry.value`
  - Sigma also uses this only for registry-related things
- `Workstation`
  - Listed as `winlog.event_data.Workstation` by elastic.com, but cannot be found anywhere in our logs
- `processPath`
  - Listed as `winlog.event_data.processPath` by elastic.com, but cannot be found anywhere in our logs
  - Guessing from the name that this is simply `process.executable`, which would align with what Sigma checks for
- `sha1`
  - Can be `hash.sha1`, `process.hash.sha1` or `filehash.sha1` according to Sigma ref, but none of them exists in our logs
  - Sometimes a sha1 hash can be found in the `message` field as well as in the `param2` field of that same log, but this is very inconsistent
  - But since related rules only trigger on a matching hash, mapping this should not have any negative consequences compared to just leaving it unmapped

### Notes regarding mapping of fields that are used by Sigma but not mentioned in any reference