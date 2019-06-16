# Some code for learning Padding Oracle Attack
There is a exploitable backend and an exploit script

# Setup
```bash
git clone https://gitlab.com/kmille/padding-oracle.git
python -m virtualenv -p python2 venv
source venv/bin/activate
cd padding-oracle
pip install -r requirements.txt

# Run the backend
source venv/bin/activate
gunicorn --bind 127.0.0.1:5000 backend:app

# Run the backend script in a new tab
source venv/bin/activate
cd padding-oracle
python exploit_backend.py # for more debug output disable some comments in oracle.Oracle.solve_oracle
```

# Example Output
<pre>
Get the encrypted message
IV:     7468697373686f756c646265726e646d
Cipher: 4eff7c78220e0a1d63439eb7707c2583d1acf7be521e2cdb7dcdd77e22676481
Let the backend decrypt the message for testing
Die ist ein beta Test
Ciphertext in hex(64): 4eff7c78220e0a1d63439eb7707c2583d1acf7be521e2cdb7dcdd77e22676481 
Ciphertext Blocks in hex: [u'4eff7c78220e0a1d63439eb7707c2583', u'd1acf7be521e2cdb7dcdd77e22676481']
Block counter: 1
Processing block #1: d1acf7be521e2cdb7dcdd77e22676481
Round counter: 0
Got no Padding Error for guess 0x89
Got intermediate byte #16: 88
All intermediates for this block: 88
Round counter: 1
Got no Padding Error for guess 0x2c
Got intermediate byte #15: 2e
All intermediates for this block: 882e
Round counter: 2
Got no Padding Error for guess 0x74
Got intermediate byte #14: 77
All intermediates for this block: 882e77
Round counter: 3
Got no Padding Error for guess 0x7f
Got intermediate byte #13: 7b
All intermediates for this block: 882e777b
Round counter: 4
Got no Padding Error for guess 0xb9
Got intermediate byte #12: bc
All intermediates for this block: 882e777bbc
Round counter: 5
Got no Padding Error for guess 0x93
Got intermediate byte #11: 95
All intermediates for this block: 882e777bbc95
Round counter: 6
Got no Padding Error for guess 0x4f
Got intermediate byte #10: 48
All intermediates for this block: 882e777bbc9548
Round counter: 7
Got no Padding Error for guess 0x60
Got intermediate byte #9: 68
All intermediates for this block: 882e777bbc954868
Round counter: 8
Got no Padding Error for guess 0x1f
Got intermediate byte #8: 16
All intermediates for this block: 882e777bbc95486816
Round counter: 9
Got no Padding Error for guess 0xb
Got intermediate byte #7: 01
All intermediates for this block: 882e777bbc9548681601
Round counter: 10
Got no Padding Error for guess 0xe
Got intermediate byte #6: 05
All intermediates for this block: 882e777bbc954868160105
Round counter: 11
Got no Padding Error for guess 0x5a
Got intermediate byte #5: 56
All intermediates for this block: 882e777bbc95486816010556
Round counter: 12
Got no Padding Error for guess 0x6
Got intermediate byte #4: 0b
All intermediates for this block: 882e777bbc954868160105560b
Round counter: 13
Got no Padding Error for guess 0x17
Got intermediate byte #3: 19
All intermediates for this block: 882e777bbc954868160105560b19
Round counter: 14
Got no Padding Error for guess 0xa4
Got intermediate byte #2: ab
All intermediates for this block: 882e777bbc954868160105560b19ab
Round counter: 15
Got no Padding Error for guess 0x7e
Got intermediate byte #1: 6e
All intermediates for this block: 882e777bbc954868160105560b19ab6e
Done with this round. Now XORING the intermediate bytes with the Cipher text of the previous ciphertext
Cipher before in hex  : 4eff7c78220e0a1d63439eb7707c2583
Recovered plain text: [' ', 'T', 'e', 's', 't', '\x0b', '\x0b', '\x0b', '\x0b', '\x0b', '\x0b', '\x0b', '\x0b', '\x0b', '\x0b', '\x0b'] 
Block counter: 0
Processing block #0: 4eff7c78220e0a1d63439eb7707c2583
Round counter: 0
Got no Padding Error for guess 0xd
Got intermediate byte #16: 0c
All intermediates for this block: 0c
Round counter: 1
Got no Padding Error for guess 0x12
Got intermediate byte #15: 10
All intermediates for this block: 0c10
Round counter: 2
Got no Padding Error for guess 0x8
Got intermediate byte #14: 0b
All intermediates for this block: 0c100b
Round counter: 3
Got no Padding Error for guess 0x14
Got intermediate byte #13: 10
All intermediates for this block: 0c100b10
Round counter: 4
Got no Padding Error for guess 0x40
Got intermediate byte #12: 45
All intermediates for this block: 0c100b1045
Round counter: 5
Got no Padding Error for guess 0xa
Got intermediate byte #11: 0c
All intermediates for this block: 0c100b10450c
Round counter: 6
Got no Padding Error for guess 0xa
Got intermediate byte #10: 0d
All intermediates for this block: 0c100b10450c0d
Round counter: 7
Got no Padding Error for guess 0x1
Got intermediate byte #9: 09
All intermediates for this block: 0c100b10450c0d09
Round counter: 8
Got no Padding Error for guess 0x5c
Got intermediate byte #8: 55
All intermediates for this block: 0c100b10450c0d0955
Round counter: 9
Got no Padding Error for guess 0x11
Got intermediate byte #7: 1b
All intermediates for this block: 0c100b10450c0d09551b
Round counter: 10
Got no Padding Error for guess 0x10
Got intermediate byte #6: 1b
All intermediates for this block: 0c100b10450c0d09551b1b
Round counter: 11
Got no Padding Error for guess 0x16
Got intermediate byte #5: 1a
All intermediates for this block: 0c100b10450c0d09551b1b1a
Round counter: 12
Got no Padding Error for guess 0x5e
Got intermediate byte #4: 53
All intermediates for this block: 0c100b10450c0d09551b1b1a53
Round counter: 13
Got no Padding Error for guess 0x2
Got intermediate byte #3: 0c
All intermediates for this block: 0c100b10450c0d09551b1b1a530c
Round counter: 14
Got no Padding Error for guess 0xe
Got intermediate byte #2: 01
All intermediates for this block: 0c100b10450c0d09551b1b1a530c01
Round counter: 15
Got no Padding Error for guess 0x20
Got intermediate byte #1: 30
All intermediates for this block: 0c100b10450c0d09551b1b1a530c0130
Done with this round. Now XORING the intermediate bytes with the Cipher text of the previous ciphertext
Cipher before in hex  : 7468697373686f756c646265726e646d
Recovered plain text: ['D', 'i', 'e', ' ', 'i', 's', 't', ' ', 'e', 'i', 'n', ' ', 'b', 'e', 't', 'a'] 
Done
Decrypted message: Die ist ein beta Test
</pre>

# Resources
 - https://en.wikipedia.org/wiki/Padding_oracle_attack

