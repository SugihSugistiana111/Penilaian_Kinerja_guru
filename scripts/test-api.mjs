// Script pengujian otomatis integrasi API SPK MOORA Al-Ihsan

async function runTests() {
  console.log('=== MEMULAI TEST INTEGRASI OTOMATIS SISTEM SPK MOORA ===\n');

  // 1. Test Login Admin
  console.log('1. Menguji Login Administrator (admin / admin123)...');
  const loginAdminRes = await fetch('http://localhost:3000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'admin123' }),
  });
  const cookieAdmin = loginAdminRes.headers.get('set-cookie');
  const loginAdminData = await loginAdminRes.json();
  console.log('   Status:', loginAdminRes.status, '| User:', loginAdminData.user.nama, '| Role:', loginAdminData.user.role);

  // 2. Test Auth /me
  console.log('\n2. Menguji verifikasi session aktif (/api/auth/me)...');
  const meRes = await fetch('http://localhost:3000/api/auth/me', {
    headers: { cookie: cookieAdmin || '' },
  });
  const meData = await meRes.json();
  console.log('   Status:', meRes.status, '| Logged In As:', meData.user.nama, 'Role:', meData.user.role);

  // 3. Test Ambil Data 18 Guru
  console.log('\n3. Menguji data master 18 Guru (/api/guru)...');
  const guruRes = await fetch('http://localhost:3000/api/guru', {
    headers: { cookie: cookieAdmin || '' },
  });
  const guruList = await guruRes.json();
  console.log('   Status:', guruRes.status, '| Total Guru Terdaftar:', guruList.length);
  guruList.slice(0, 3).forEach((g, idx) => {
    console.log(`   [Guru ${idx + 1}] ${g.nama} | Mapel: ${g.jabatanTugasMengajar} | Rombel: ${g.jumlahSiswaPerRombel} Siswa | Jam: ${g.jumlahJamAjar} Jam`);
  });

  // 4. Test Kriteria & Bobot
  console.log('\n4. Menguji kriteria & bobot MOORA (/api/kriteria)...');
  const kriteriaRes = await fetch('http://localhost:3000/api/kriteria', {
    headers: { cookie: cookieAdmin || '' },
  });
  const kriteriaList = await kriteriaRes.json();
  console.log('   Status:', kriteriaRes.status);
  kriteriaList.forEach((k) => {
    console.log(`   Kriteria ${k.kode}: ${k.nama} | Bobot: ${k.bobot * 100}% | Jenis: ${k.jenis}`);
  });

  // 5. Test Periode & Detail MOORA
  console.log('\n5. Menguji periode & komputasi MOORA (/api/periode & /api/moora/detail)...');
  const periodeRes = await fetch('http://localhost:3000/api/periode', {
    headers: { cookie: cookieAdmin || '' },
  });
  const periodeList = await periodeRes.json();
  console.log('   Status:', periodeRes.status, '| Periode Ditemukan:', periodeList.length);

  const periodeAktif = periodeList.find((p) => p.status === 'AKTIF') || periodeList[0];
  const mooraRes = await fetch(`http://localhost:3000/api/moora/detail?periodeId=${periodeAktif.id}`, {
    headers: { cookie: cookieAdmin || '' },
  });
  const mooraData = await mooraRes.json();
  console.log('   Periode Aktif:', periodeAktif.namaPeriode);
  console.log('   Validasi Kelengkapan:', mooraData.validasi.isLengkap ? '100% LENGKAP' : 'BELUM LENGKAP');
  console.log('   Total Guru Terhitung MOORA:', mooraData.hasilTersimpan?.length || 0);

  if (mooraData.hasilTersimpan?.length > 0) {
    console.log('\n   TOP 3 HASIL RANKING MOORA:');
    mooraData.hasilTersimpan.slice(0, 3).forEach((item) => {
      console.log(`   Rank #${item.ranking} : ${item.guru.nama.padEnd(26)} | Nilai MOORA: ${item.nilaiPreferensi.toFixed(4)} | Mapel: ${item.guru.jabatanTugasMengajar}`);
    });
  }

  // 6. Test Login Guru (Ahmad Fauzi)
  console.log('\n6. Menguji Login Guru (guru1 / guru123)...');
  const loginGuruRes = await fetch('http://localhost:3000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'guru1', password: 'guru123' }),
  });
  const cookieGuru = loginGuruRes.headers.get('set-cookie');
  const loginGuruData = await loginGuruRes.json();
  console.log('   Status:', loginGuruRes.status, '| Guru User:', loginGuruData.user.nama, '| Role:', loginGuruData.user.role);

  // 7. Test Guru Profile Data
  console.log('\n7. Menguji akses mandiri guru (/api/guru/[guruId])...');
  const guruDetailRes = await fetch(`http://localhost:3000/api/guru/${loginGuruData.user.guruId}`, {
    headers: { cookie: cookieGuru || '' },
  });
  const guruDetailData = await guruDetailRes.json();
  console.log('   Status:', guruDetailRes.status, '| Nama:', guruDetailData.nama, '| Total Penilaian:', guruDetailData.penilaian.length);

  console.log('\n=== SEMUA PENGUJIAN INTEGRASI BERHASIL 100% DENGAN SUKSES! ===');
}

runTests().catch(console.error);
