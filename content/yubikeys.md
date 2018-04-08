Title:  My YubiKey Quickstart guide
Date: 2016-06-13 23:00
Modified: 2016-06-15 00:30
Tags: security
Status: published
Summary: My YubiKey Quickstart guide - what you can do with yours/what do I do?

![yubikey-photo](https://farm3.staticflickr.com/2625/3689896409_35043dc8ba_d.jpg)

It's been a while I'm thinking to step in the smart card world. It's been years I've got a smart card on me all the time. I only use it once a year, for paying my taxes... Everytime I use it, I'm complaining. A lot.

Here are a few reasons for it:

1. Everything linked to its usage as a smart card is poorly documented. I really hope it's not by design.
1. It requires specific hardware: a special kind of smart card reader (so not every smart card reader works!)
1. It requires specific software: a specific version of java (use java64 for an unreliable/unpleasant experience!), and sometimes even your version of java32 doesn't work with it
1. It doesn't work on all the browsers! You need to have a specific plugin. Of course, if you insert your smart card **AFTER** launching Firefox, you're good for its restart.
1. You can't do whatever you want with it (can't set your own keys ...)

Taxes feeling + grumpy {soft,hard}ware makes me unhappy. It's unlikely I'll use this smartcard in other circumstances (anyway, it's maybe better -_security wise_- to avoid mixing the same device for different security purposes).

So, I decided to give YubiKeys a go.

## What are YubiKeys, and why would I want one?

I recently found the YubiKeys more interesting.
The YubiKey 4 packs a big list of features, for a really low cost. Moreover, there is currently a 20% discount for github users on yubico website ("temporary offer").

In terms of (hardware) requirements, you only need a good ol' USB port to work. The YubiKey Neo adds [NFC](https://en.wikipedia.org/wiki/Near_field_communication) to the mix for your mobile (but the Neo have drawbacks, check the cypto specs here: <https://www.yubico.com/products/yubikey-hardware/>). For your information, the Neo is currently cheaper on amazon than it is on yubico website.

In terms of features, the YubiKey works as [HID](https://en.wikipedia.org/wiki/USB_human_interface_device_class) for [**2-F**actor **A**uthentication](https://en.wikipedia.org/wiki/Two-factor_authentication) mechanisms ([fido u2fa][fido-u2fa], yubico OTP, ...) and it also works as [CCID](https://en.wikipedia.org/wiki/CCID_(protocol)) (smartcards! you can use it for signing, encryption, authentication with applications like [pgp](https://en.wikipedia.org/wiki/Pretty_Good_Privacy), [openssh](https://en.wikipedia.org/wiki/OpenSSH), [openssl](https://en.wikipedia.org/wiki/OpenSSL) and many others).

## Ok I'm in! Where should I start ?

Simple question, long answer. Don't start with the "documentation" of the [dev.yubico][] website!
There is so much documentation on their website, you'll be lost in all the links.

Here is what I'd do:

1. Simply start on your device page ([yubikey 4][]/[yubikey neo][]) and absorb what's there.
1. You should then find the [getting started page][yubico-start] interesting.
1. You should then go ahead with the [personalisation tools page][yubico-pt-page].

You have plenty links on these three pages to follow what's really needed to your use case. The last page of this list have obviously a link for the [yubico personalisation tool][yubico-pt] download. This tool makes possible in-depth changes of your YubiKey.

## Any other links?

For github/google, simply head to your account security settings. [U2FA][fido-u2fa] is very simple and doesn't really need much explanation. You don't need the personalisation tool to make it work. For non-U2FA, that's where the fun begins...

Here are a few interesting explanations I found by browsing the interwebz/yubico website:

- [Configuring Yubikey as generic OATH HOTP token generator][generic-hotp]. I read somewhere was possible to enable this kind of 2FA on Ubuntu One website, but I didn't find the option there yet.
- [Configuring YubiKey as a smartcard for ssh authentication, CA or code signing][ssh-cert]. On this page, you should probably have a look at the SSH with PIV and PKCS#11 section. It's easy to use a certificate stored on the yubikey for SSH authentication: you just have to pass the library interface ([opensc](https://en.wikipedia.org/wiki/OpenSC)) to the [PKCS#11][] as identity in your openssh command line. This is supported with a portable openssh version > 5.4p1. (It's also easy to export your public key to set it in the authorized keys for example). Check also [here][piv-slots] for an explanation of your Yubikey's PIV slots.
- Configuring PAM and SSH server for a 2FA with Yubico OTP ([1][] [2][] [3][] [4][] ). Take these with a pinch of salt (Some pages claim to improve security by using their method, where it clearly doesn't. More on that in a later article).
- [Configuring PGP with YubiKeys][pgp]. This is where you should head to for file encryption, mail encryption/signing, ssh authentication...

## Last words

I think the YubiKey is a simple yet efficient device. It protects your accounts
in a simple manner, and everyone interested in security should at least consider
it (or one of its alternatives).

[dev.yubico]: https://developers.yubico.com/
[yubikey 4]: http://yubi.co/4
[yubikey neo]: https://www.yubico.com/products/yubikey-hardware/yubikey-neo/
[yubico-start]: https://www.yubico.com/start/
[yubico-pt]: https://www.yubico.com/pt
[yubico-pt-page]: https://www.yubico.com/products/services-software/personalization-tools/
[generic-hotp]: https://www.yubico.com/products/services-software/personalization-tools/oath/
[ssh-cert]: https://developers.yubico.com/PIV/Guides/SSH_with_PIV_and_PKCS11.html
[piv-slots]: https://developers.yubico.com/PIV/Introduction/Certificate_slots.html
[1]: https://derekriemer.com/2017/02/11/how-i-rolled-two-factor-authentication-for-ssh-access-to-the-server-that-powers-this-site/
[2]: http://delyan.me/securing-ssh-with-totp/
[3]: https://www.100tb.com/blog/ssh-two-factor-authentication-with-totp-in-debianubuntu/
[4]: http://strugglers.net/~andy/blog/2016/05/06/using-a-totp-app-for-multi-factor-ssh-auth/
[pgp]: https://developers.yubico.com/PGP/
[fido-u2fa]: https://en.wikipedia.org/wiki/Universal_2nd_Factor
[PKCS#11]: https://en.wikipedia.org/wiki/PKCS_11

*Photo credit: [Thomas Flenstad](https://www.flickr.com/photos/11506685@N07/3689896409/)*
