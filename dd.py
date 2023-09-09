  {
    rabbit,
    [
      {ssl_listeners, [5671]},
      {ssl_options, [
        {cacertfile, "/root/example.com.crt"},
        {certfile, "/root/example.com.crt"},
        {keyfile, "/root/example.com.key"},
        {verify, verify_none},
        {fail_if_no_peer_cert, false}
      ]}
    ]
  }
].
